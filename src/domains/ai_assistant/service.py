from sqlalchemy.orm import Session

from src.domains.product.models import Product

from src.models.saas_core import (
    Order,
    Customer,
)

from src.domains.ai.services.memory_service import get_ai_memory


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

    memories = get_ai_memory(
        db,
        tenant_id,
        5
    )

    text = message.lower()

    if (
        "business" in text
        or "လုပ်ငန်း" in text
        or "အခြေအနေ" in text
        or "summary" in text
    ):

        memory_text = ""

        for m in memories:
            memory_text += f"\n- {m.content}"

        return (
            f"""
📊 Business Summary

🛒 Orders: {data['orders']} ခု

👥 Customers: {data['customers']} ယောက်

📦 Products: {data['products']} ခု


🤖 AI Memory:
{memory_text}


လုပ်ငန်းအခြေအနေကို ဆက်လက်စောင့်ကြည့်နေပါတယ်။
""",
            "BUSINESS_ANALYSIS"
        )


    if "product" in text or "ပစ္စည်း" in text:
        return (
            f"Product စုစုပေါင်း {data['products']} ခုရှိပါတယ်။",
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
