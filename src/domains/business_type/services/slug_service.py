import re


def generate_business_slug(name: str):

    slug = name.lower()

    slug = re.sub(
        r"[^a-z0-9\s-]",
        "",
        slug
    )

    slug = re.sub(
        r"\s+",
        "-",
        slug
    )

    slug = slug.strip("-")

    return slug
