from pathlib import Path

p = Path("src/models/saas_core.py")
s = p.read_text()

if "class CustomerPayment(Base):" in s:
    print("ALREADY EXISTS")
    exit()

insert = '''

class CustomerPayment(Base):
    __tablename__ = "customer_payments"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    payment_number = Column(
        String,
        nullable=False,
        index=True
    )

    customer_id = Column(
        String,
        ForeignKey("customers.id"),
        nullable=False
    )

    receivable_id = Column(
        String,
        ForeignKey("receivables.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        default="CASH"
    )

    status = Column(
        String,
        default="COMPLETED"
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

'''

marker = "class Receivable(Base):"

if marker in s:
    s = s.replace(marker, insert + "\n" + marker)
    p.write_text(s)
    print("CUSTOMER PAYMENT MODEL ADDED")
else:
    print("MARKER NOT FOUND")
