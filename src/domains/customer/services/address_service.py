from sqlalchemy.orm import Session

from src.models.saas_core import CustomerAddress
from src.domains.customer.contracts.address_contract import AddressContext


class CustomerAddressService:
    """
    Customer Address Runtime Capability.

    Core customer domain only.
    """

    @staticmethod
    def create_address(
        db: Session,
        tenant_id: str,
        context: AddressContext,
    ):

        address = CustomerAddress(
            tenant_id=tenant_id,
            customer_id=context.customer_id,
            address_type=context.address_type,
            line1=context.line1,
            city=context.city,
            township=context.township,
            phone=context.phone,
        )

        db.add(address)
        db.commit()
        db.refresh(address)

        return address


    @staticmethod
    def get_customer_addresses(
        db: Session,
        customer_id: str,
        tenant_id: str,
    ):

        return (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.tenant_id == tenant_id,
            )
            .all()
        )


    @staticmethod
    def delete_address(
        db: Session,
        address_id: str,
        tenant_id: str,
    ):

        address = (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.id == address_id,
                CustomerAddress.tenant_id == tenant_id,
            )
            .first()
        )

        if not address:
            return None

        db.delete(address)
        db.commit()

        return {
            "status": "deleted",
            "id": address_id,
        }
