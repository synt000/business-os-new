from abc import ABC, abstractmethod


class PaymentProvider(ABC):

    @abstractmethod
    def create_payment(
        self,
        amount: float,
        reference: str
    ):
        pass


    @abstractmethod
    def verify_payment(
        self,
        transaction_ref: str
    ):
        pass
