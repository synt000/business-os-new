from pathlib import Path

path = Path("src/domains/social_center/router.py")

lines = path.read_text().splitlines()

output = []

inserted_import = False
patched = False

for line in lines:

    if (
        line.startswith("from src.application.channel.resolver import")
        and not inserted_import
    ):
        inserted_import = True

    output.append(line)

    if (
        inserted_import
        and line.strip() == ")"
        and "IdentityRuntime" not in "\n".join(lines)
    ):
        output.extend([
            "",
            "from src.application.identity.runtime import IdentityRuntime",
            "from src.domains.customer.contracts.identity_contract import (",
            "    IdentityContext,",
            ")",
            "from src.domains.customer.contracts.identity_resolution_contract import (",
            "    IdentityResolutionRequest,",
            ")",
        ])
        inserted_import = False


text = "\n".join(output)


old = """                    customer_id=sender_id,
                    message=message_text
                  )"""

new = """                    customer_id=resolved_customer_id,
                    message=message_text
                  )"""


if old not in text:
    raise SystemExit("CUSTOMER ID TARGET NOT FOUND")


text = text.replace(
    old,
    """                    customer_id=resolved_customer_id,
                    message=message_text
                  )"""
)


marker = """              if channel:
"""

if marker not in text:
    raise SystemExit("CHANNEL BLOCK NOT FOUND")


inject = """              if channel:

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
"""


start = text.index(marker)

save_pos = text.index(
    "                  SocialCenterService.save_message(",
    start
)

text = (
    text[:start]
    + inject
    + text[save_pos:]
)


path.write_text(text)

print("PHASE 7.4-C1 PATCH APPLIED")
