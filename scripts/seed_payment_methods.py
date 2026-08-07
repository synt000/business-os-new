from src.core.database import SessionLocal
from src.domains.payment.models import PaymentMethod


DEFAULT_PAYMENT_METHODS = [
    {
        "code": "CASH",
        "name": "Cash Payment",
        "category": "CASH",
        "ledger_account": "CASH_ASSET",
    },
    {
        "code": "KBZ_BANK",
        "name": "KBZ Bank",
        "category": "BANK",
        "ledger_account": "BANK_ASSET",
    },
    {
        "code": "AYA_BANK",
        "name": "AYA Bank",
        "category": "BANK",
        "ledger_account": "BANK_ASSET",
    },
    {
        "code": "CB_BANK",
        "name": "CB Bank",
        "category": "BANK",
        "ledger_account": "BANK_ASSET",
    },
    {
        "code": "CB_ATM",
        "name": "CB ATM",
        "category": "BANK",
        "ledger_account": "BANK_ASSET",
    },
    {
        "code": "WAVE_MONEY",
        "name": "Wave Money",
        "category": "DIGITAL",
        "ledger_account": "DIGITAL_ASSET",
    },
    {
        "code": "KPAY",
        "name": "KPay",
        "category": "DIGITAL",
        "ledger_account": "DIGITAL_ASSET",
    },
]


def seed():
    db = SessionLocal()

    try:
        for item in DEFAULT_PAYMENT_METHODS:

            exists = (
                db.query(PaymentMethod)
                .filter(
                    PaymentMethod.code == item["code"]
                )
                .first()
            )

            if exists:
                print("SKIP:", item["code"])
                continue

            method = PaymentMethod(**item)

            db.add(method)

            print("ADD:", item["code"])

        db.commit()

        print("PAYMENT METHOD SEED COMPLETE")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
