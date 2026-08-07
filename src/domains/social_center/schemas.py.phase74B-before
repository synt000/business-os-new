from pydantic import BaseModel


class BusinessProfileCreate(BaseModel):

    business_name: str
    logo_url: str | None = None
    phone: str | None = None
    address: str | None = None
    description: str | None = None



class SocialAccountCreate(BaseModel):

    platform: str
    account_name: str | None = None
    account_url: str | None = None



class SocialAccountResponse(BaseModel):

    id: str
    platform: str
    account_name: str | None
    account_url: str | None
    status: str


    class Config:
        from_attributes = True


class SocialMessageResponse(BaseModel):
    id: str
    platform: str
    customer_name: str | None = None
    customer_id: str | None = None
    message: str | None = None
    message_type: str | None = None
    status: str
    reply_text: str | None = None
    created_at: object | None = None

    class Config:
        from_attributes = True


class SocialLeadStatusUpdate(BaseModel):
    status: str


class SocialLeadResponse(BaseModel):
    id: str
    customer_name: str | None = None
    customer_phone: str | None = None
    source: str
    platform: str
    message_id: str | None = None
    status: str
    created_at: object | None = None

    class Config:
        from_attributes = True
