from abc import ABC, abstractmethod


class IndustryTemplate(ABC):
    """
    Base contract for Industry Templates.
    Industry layer only.
    """

    key: str = ""
    name: str = ""

    @abstractmethod
    def capabilities(self) -> list[str]:
        """
        Return supported capability keys.
        """
        pass
