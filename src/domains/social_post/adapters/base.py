from abc import ABC, abstractmethod


class SocialPublisherAdapter(ABC):

    @abstractmethod
    def publish(
        self,
        content: str,
        media_url: str | None = None
    ):
        pass
