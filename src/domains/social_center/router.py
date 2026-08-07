from fastapi import APIRouter, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.domains.social_center.service import (
    SocialCenterService,
)

from src.domains.social_center.schemas import (
    SocialChannelCreate,
)

from src.application.channel.contracts import (
    ChannelResolutionRequest,
)

from src.application.channel.resolver import (
    ChannelResolver,
)


router = APIRouter(
    prefix="/api/v4/social",
    tags=["Social Center"]
)


@router.get("/channels")
def channels(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return SocialCenterService.list_channels(
        db,
        current_user.tenant_id
    )


@router.post("/channels")
def create_channel(
    data: SocialChannelCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return SocialCenterService.create_channel(
        db,
        current_user.tenant_id,
        data
    )



@router.get("/facebook/webhook")
def verify_webhook(
    hub_mode: str = "",
    hub_verify_token: str = "",
    hub_challenge: str = ""
):

    if hub_verify_token == "business_os_verify":
        return int(hub_challenge)

    return {
        "status": "invalid"
    }


@router.post("/facebook/webhook")
async def receive_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    payload = await request.json()


    try:

        entry = payload.get("entry", [])[0]

        messaging = entry.get(
            "messaging",
            []
        )[0]


        sender_id = (
            messaging
            .get("sender", {})
            .get("id")
        )

        recipient_id = (
            messaging
            .get("recipient", {})
            .get("id")
        )

        message_text = (
            messaging
            .get("message", {})
            .get("text")
        )


        if sender_id and message_text:

            resolution = ChannelResolver.resolve(
                db=db,
                request=ChannelResolutionRequest(
                    provider="facebook",
                    external_channel_id=recipient_id or "",
                ),
            )

            if not resolution.resolved:
                return {
                    "status": "received",
                    "message": "CHANNEL_NOT_RESOLVED",
                }

            tenant_context = resolution.tenant_context

            channel = (
                db.query(
                    __import__(
                        "src.domains.social_center.models",
                        fromlist=[
                            "SocialChannel"
                        ]
                    ).SocialChannel
                )
                .filter(
                    __import__(
                        "src.domains.social_center.models",
                        fromlist=[
                            "SocialChannel"
                        ]
                    ).SocialChannel.platform
                    == "facebook",
                    __import__(
                        "src.domains.social_center.models",
                        fromlist=[
                            "SocialChannel"
                        ]
                    ).SocialChannel.external_id
                    == recipient_id,
                    __import__(
                        "src.domains.social_center.models",
                        fromlist=[
                            "SocialChannel"
                        ]
                    ).SocialChannel.tenant_id
                    == tenant_context.tenant_id,
                )
                .first()
            )


            if channel:

                SocialCenterService.save_message(
                    db=db,
                    tenant_id=channel.tenant_id,
                    platform="facebook",
                    customer_name="Facebook User",
                    customer_id=sender_id,
                    message=message_text
                )


    except Exception as e:

        print(
            "FACEBOOK WEBHOOK ERROR:",
            e
        )


    return {
        "status": "received"
    }


@router.get("/messages")
def messages(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return SocialCenterService.list_messages(
        db,
        current_user.tenant_id
    )



@router.get("/messages/unread")
def unread_messages(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return SocialCenterService.unread_messages(
        db,
        current_user.tenant_id
    )



@router.post("/messages/{message_id}/reply")
def reply_message(
    message_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    reply_text = payload.get("reply_text")

    result = SocialCenterService.update_reply(
        db,
        current_user.tenant_id,
        message_id,
        reply_text
    )

    if not result:
        return {
            "status":"not_found"
        }


    return {
        "status":"replied",
        "message_id": message_id,
        "reply_id": result.get("reply_id")
    }



@router.get("/messages/{message_id}/history")
def reply_history(
    message_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    from src.models.saas_core import (
        SocialMessageReply,
        SocialReplyAttachment
    )

    rows = (
        db.query(SocialMessageReply)
        .filter(
            SocialMessageReply.message_id == message_id,
            SocialMessageReply.tenant_id == current_user.tenant_id
        )
        .order_by(
            SocialMessageReply.created_at.asc()
        )
        .all()
    )

    result = []

    for reply in rows:

        attachments = (
            db.query(SocialReplyAttachment)
            .filter(
                SocialReplyAttachment.reply_id == reply.id,
                SocialReplyAttachment.tenant_id == current_user.tenant_id
            )
            .all()
        )

        result.append({
            "id": reply.id,
            "reply_text": reply.reply_text,
            "replied_by": reply.replied_by,
            "created_at": reply.created_at,
            "attachments": [
                {
                    "url": a.file_url,
                    "name": a.file_name,
                    "type": a.file_type
                }
                for a in attachments
            ]
        })

    return result





# OLD MESSAGE ATTACHMENT ROUTE REMOVED

@router.post("/replies/{reply_id}/attachment")
async def upload_reply_attachment(
    reply_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    import uuid
    from pathlib import Path
    import shutil

    ALLOWED_EXTENSIONS={
        "jpg","jpeg","png","gif","webp",
        "mp3","wav","ogg",
        "pdf",
        "xlsx","xls",
        "docx","doc",
        "txt"
    }

    BLOCKED_EXTENSIONS={
        "php","py","exe","sh","html",
        "htm","js","svg","bat","cmd"
    }

    ext=file.filename.rsplit(".",1)[-1].lower() if "." in file.filename else ""

    if ext in BLOCKED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Blocked file type"
        )

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    data=await file.read()

    MAX_SIZE=20*1024*1024

    if len(data)>MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    file.file.seek(0)

    upload_dir = Path(
        "src/static/uploads/social"
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    import re

    safe_name=re.sub(
        r"[^A-Za-z0-9._-]",
        "_",
        file.filename
    )

    filename=(
        str(uuid.uuid4())
        +
        "_"
        +
        safe_name
    )

    filepath = upload_dir / filename

    with filepath.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    from src.models.saas_core import SocialReplyAttachment

    attachment = SocialReplyAttachment(
        id=str(uuid.uuid4()),
        reply_id=reply_id,
        file_url="/static/uploads/social/" + filename,
        file_name=file.filename,
        file_type=file.content_type,
        tenant_id=current_user.tenant_id
    )

    db.add(attachment)
    db.commit()


    return {
        "status":"uploaded",
        "reply_id": reply_id,
        "url": attachment.file_url,
        "name": attachment.file_name,
        "type": attachment.file_type
    }


@router.get("/conversations/{customer_id}")
def conversation(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return {
        "customer_id": customer_id,
        "messages": SocialCenterService.get_conversation(
            db,
            current_user.tenant_id,
            customer_id
        )
    }



@router.post("/messages/read/{customer_id}")
def mark_messages_read(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return SocialCenterService.mark_read(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )



@router.get("/customer/{customer_id}")
def customer_profile(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return SocialCenterService.customer_profile(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )

