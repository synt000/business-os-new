
class WavePayProvider:


    def create_payment(
        self,
        amount,
        reference
    ):

        return {
            "provider":"WAVEPAY",
            "amount":amount,
            "reference":reference,
            "status":"PENDING"
        }


    def verify_payment(
        self,
        payload
    ):

        return {
            "provider":"WAVEPAY",
            "verified":True,
            "reference":payload.get(
                "reference"
            )
        }

