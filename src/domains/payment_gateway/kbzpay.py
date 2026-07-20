
class KBZPayProvider:


    def create_payment(
        self,
        amount,
        reference
    ):

        return {
            "provider":"KBZPAY",
            "amount":amount,
            "reference":reference,
            "status":"PENDING"
        }


    def verify_payment(
        self,
        payload
    ):

        return {
            "provider":"KBZPAY",
            "verified":True,
            "reference":payload.get(
                "reference"
            )
        }

