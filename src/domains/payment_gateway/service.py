from src.domains.payment_gateway.kbzpay import KBZPayProvider
from src.domains.payment_gateway.wavepay import WavePayProvider


class PaymentGatewayService:


    providers = {
        "KBZPAY": KBZPayProvider(),
        "WAVEPAY": WavePayProvider()
    }


    @staticmethod
    def create_payment(
        provider,
        amount,
        reference
    ):

        gateway = PaymentGatewayService.providers.get(
            provider.upper()
        )

        if not gateway:
            raise Exception(
                "PAYMENT_PROVIDER_NOT_SUPPORTED"
            )


        return gateway.create_payment(
            amount,
            reference
        )


    @staticmethod
    def verify_payment(
        provider,
        payload
    ):

        gateway = PaymentGatewayService.providers.get(
            provider.upper()
        )

        if not gateway:
            raise Exception(
                "PAYMENT_PROVIDER_NOT_SUPPORTED"
            )


        return gateway.verify_payment(
            payload
        )
