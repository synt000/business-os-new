from sqlalchemy.orm import Session
from src.domains.product.models import Product

from src.models.saas_core import (
    Order,
    Customer,
)


def analyze_business(
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


    customers = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
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


    return {
        "products": products,
        "customers": customers,
        "orders": orders,
    }



def ask_ai(
    db: Session,
    tenant_id: str,
    message: str
):

    data = analyze_business(
        db,
        tenant_id
    )


    text = message.lower()


    if "product" in text or "ပစ္စည်း" in text:

        return (
            "PRODUCT"
        )


    if "customer" in text or "ဖောက်သည်" in text:

        return (
            f"Customer စုစုပေါင်း {data['customers']} ယောက်ရှိပါတယ်။",
            "CUSTOMER"
        )


    if "order" in text or "အော်ဒါ" in text:

        return (
            f"Order စုစုပေါင်း {data['orders']} ခုရှိပါတယ်။",
            "ORDER"
        )


    return (
        "AI Assistant က သင့်လုပ်ငန်း Data ကို စစ်ဆေးနေပါတယ်။",
        "GENERAL"
    )
