from src.domains.industry.online_shop.template import OnlineShopTemplate


INDUSTRY_REGISTRY = {
    OnlineShopTemplate.key: OnlineShopTemplate,
}


def get_industry_template(industry_key: str):
    if not industry_key:
        return None

    industry_key = industry_key.upper()

    template = INDUSTRY_REGISTRY.get(industry_key)

    if not template:
        return None

    return template()
