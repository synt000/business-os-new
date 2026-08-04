from src.domains.industry.base import IndustryTemplate
from .capabilities import ONLINE_SHOP_CAPABILITIES


class OnlineShopTemplate(IndustryTemplate):

    key = "ONLINE_SHOP"

    name = "Online Shop"

    def capabilities(self) -> list[str]:
        return ONLINE_SHOP_CAPABILITIES
