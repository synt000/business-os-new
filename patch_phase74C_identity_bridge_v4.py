from pathlib import Path

path = Path("src/domains/social_center/router.py")

lines = path.read_text().splitlines()

new_lines = []

added_import = False
identity_added = False

for line in lines:

    if (
        line.strip() == "from src.application.channel.resolver import ("
        and not added_import
    ):
        pass

    new_lines.append(line)

    if (
        line.strip() == "if channel:"
        and not identity_added
    ):
        new_lines.extend([
            "",
            "                  identity_result = IdentityRuntime.resolve(",
            "                      db=db,",
            "                      request=IdentityResolutionRequest(",
            "                          tenant_context=tenant_context,",
            "                          identity_context=IdentityContext(",
            "                              provider=\"facebook\",",
            "                              external_user_id=sender_id,",
            "                          ),",
            "                      ),",
            "                  )",
            "",
            "                  resolved_customer_id = (",
            "                      identity_result.customer_id",
            "                      if identity_result",
            "                      else None",
            "                  )",
        ])
        identity_added = True


result = []

for line in new_lines:

    if "from src.application.identity.runtime import IdentityRuntime" in "\n".join(result):
        result.append(line)
        continue

    if line.strip() == "customer_id=sender_id,":
        result.append(
            line.replace(
                "customer_id=sender_id",
                "customer_id=resolved_customer_id"
            )
        )
    else:
        result.append(line)


text = "\n".join(result)

if not identity_added:
    raise SystemExit("IDENTITY INSERT FAILED")

path.write_text(text)

print("PHASE 7.4-C1 LINE PATCH APPLIED")
