from pathlib import Path

path = Path("src/domains/social_center/router.py")

text = path.read_text()

# Add imports
old = """from src.application.channel.resolver import (
    ChannelResolver,
)
"""

new = """from src.application.channel.resolver import (
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

if old in text and "IdentityRuntime" not in text:
    text = text.replace(old, new)


# Insert identity resolve before save_message
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
    raise SystemExit(
        "TARGET BLOCK NOT FOUND - STOP"
    )

text = text.replace(old, new)

path.write_text(text)

print("PHASE 7.4-C1 PATCH APPLIED")
