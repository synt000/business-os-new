from pathlib import Path

path = Path("src/domains/social_center/router.py")

text = path.read_text()

if "from src.application.identity.runtime import IdentityRuntime" not in text:

    marker = """from src.application.channel.resolver import (
    ChannelResolver,
)
"""

    insert = """from src.application.channel.resolver import (
    ChannelResolver,
)

from src.application.identity.runtime import IdentityRuntime
from src.domains.customer.contracts.identity_contract import (
    IdentityContext,
)
from src.domains.customer.contracts.identity_resolution_contract import (
    IdentityResolutionRequest,
)
"""

    if marker not in text:
        raise SystemExit("IMPORT TARGET NOT FOUND")

    text = text.replace(marker, insert)


old = """              if channel:

                  SocialCenterService.save_message(
                      db=db,
                      tenant_id=channel.tenant_id,
                      platform="facebook",
                      customer_name="Facebook User",
                      customer_id=sender_id,
                      message=message_text
                  )
"""

new = """              if channel:

                  identity_result = IdentityRuntime.resolve(
                      db=db,
                      request=IdentityResolutionRequest(
                          tenant_context=tenant_context,
                          identity_context=IdentityContext(
                              provider="facebook",
                              external_user_id=sender_id,
                          ),
                      ),
                  )

                  resolved_customer_id = (
                      identity_result.customer_id
                      if identity_result
                      else None
                  )

                  SocialCenterService.save_message(
                      db=db,
                      tenant_id=channel.tenant_id,
                      platform="facebook",
                      customer_name="Facebook User",
                      customer_id=resolved_customer_id,
                      message=message_text
                  )
"""

if old not in text:
    raise SystemExit("SAVE MESSAGE TARGET NOT FOUND")

text = text.replace(old, new)

path.write_text(text)

print("PHASE 7.4-C1 IDENTITY BRIDGE PATCH APPLIED")
