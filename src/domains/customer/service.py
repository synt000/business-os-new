from sqlalchemy.orm import Session
from .models import Customer
from .schemas import CustomerCreate


class CustomerService:


    @staticmethod
    def create(
        db: Session,
        tenant_id: str,
        payload: CustomerCreate
    ):

        customer = Customer(
        tenant_id=tenant_id,
        customer_name=payload.name,
        customer_phone=payload.phone,
        customer_email=payload.email
    )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer


    @staticmethod
    def list(
        db: Session,
        tenant_id: str
    ):

        return db.query(Customer).filter(
            Customer.tenant_id == tenant_id
        ).all()


    @staticmethod
    def get(
        db: Session,
        customer_id: str,
        tenant_id: str
    ):
        return db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        ).first()


    @staticmethod
    def update(
        db: Session,
        customer_id: str,
        tenant_id: str,
        payload: CustomerCreate
    ):
        customer = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        ).first()

        customer.customer_name = payload.name
        customer.customer_phone = payload.phone
        customer.customer_email = payload.email

        db.commit()
        db.refresh(customer)

        return customer


    @staticmethod
    def delete(
        db: Session,
        customer_id: str,
        tenant_id: str
    ):
        customer = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        ).first()

        db.delete(customer)
        db.commit()

        return {
            "status":"deleted",
            "id":customer_id
        }


    @staticmethod
    def analytics(
        db: Session,
        customer_id: str,
        tenant_id: str
    ):

        customer = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        ).first()


        if not customer:
            return None


        return {
            "id": customer.id,
            "name": customer.customer_name,
            "phone": customer.customer_phone,
            "email": customer.customer_email,
            "total_spent": customer.total_spent or 0,
            "total_orders": len(customer.orders) if customer.orders else 0,
            "rank":
                "Gold"
                if (customer.total_spent or 0) >= 1000000
                else "Silver"
                if (customer.total_spent or 0) >= 500000
                else "Bronze"
        }



    @staticmethod
    def orders(
        db: Session,
        customer_id: str,
        tenant_id: str
    ):

        customer = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        ).first()


        if not customer:
            return []


        return [
            {
                "id": order.id,
                "order_number": order.order_number,
                "amount": order.total_amount or 0,
                "status": order.order_status,
                "created_at": order.created_at
            }
            for order in customer.orders
        ]


    @staticmethod
    def revenue(
        db: Session,
        customer_id: str,
        tenant_id: str
    ):

        orders = CustomerService.orders(
            db,
            customer_id,
            tenant_id
        )

        return {
            "customer_id": customer_id,
            "total_orders": len(orders),
            "total_revenue": sum(
                o["amount"] for o in orders
            )
        }

