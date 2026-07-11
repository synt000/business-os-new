from sqlalchemy.orm import Session

from src.models.saas_core import (
    Product,
    Order,
    Customer,
    Supplier,
)


class DashboardService:

    """
    Enterprise Dashboard Metrics

    Tenant isolated summary engine
    """

    @staticmethod
    def get_summary(
        db: Session,
        tenant_id: str
    ):

        products = (
            db.query(Product)
            .filter(
                Product.tenant_id == tenant_id
            )
            .count()
        )


        orders = (
            db.query(Order)
            .filter(
                Order.tenant_id == tenant_id
            )
            .count()
        )


        customers = (
            db.query(Customer)
            .filter(
                Customer.tenant_id == tenant_id
            )
            .count()
        )


        suppliers = (
            db.query(Supplier)
            .filter(
                Supplier.tenant_id == tenant_id
            )
            .count()
        )


        return {
            "products": products,
            "orders": orders,
            "customers": customers,
            "suppliers": suppliers
        }
