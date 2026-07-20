from sqlalchemy.orm import Session

from src.domains.product.models import Product
from src.domains.purchase.models import SupplierPayable

from src.models.saas_core import (
    Order,
    Payment,
)

from src.domains.ai.services.memory_service import save_ai_memory


def generate_ai_recommendations(
    db: Session,
    tenant_id: str
):

    recommendations = []


    # ==========================
    # STOCK RECOMMENDATION
    # ==========================

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )


    for product in products:

        stock = 0

        if product.inventory:
            stock = product.inventory.quantity


        if stock <= 0:

            recommendations.append({
                "title": "Urgent Stock Purchase",
                "priority": "HIGH",
                "action":
                f"{product.name} stock 0 ဖြစ်နေပါသည်။ Purchase Order တင်ရန် အကြံပြုပါသည်"
            })


        elif stock <= product.reorder_level:

            recommendations.append({
                "title": "Low Stock Warning",
                "priority": "MEDIUM",
                "action":
                f"{product.name} လက်ကျန် {stock} ခုသာရှိပါသည်။ Stock ဖြည့်ရန် စီစဉ်ပါ"
            })



    # ==========================
    # SUPPLIER DEBT
    # ==========================

    payables = (
        db.query(SupplierPayable)
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .all()
    )


    debt = sum(
        x.balance_amount or 0
        for x in payables
    )


    if debt > 0:

        recommendations.append({
            "title": "Cash Flow Control",
            "priority": "MEDIUM",
            "action":
            f"Supplier အကြွေး {debt} ရှိပါသည်။ Payment Plan စီမံရန် အကြံပြုပါသည်"
        })



    # ==========================
    # SALES ANALYSIS
    # ==========================

    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id
        )
        .count()
    )


    if orders > 0:

        recommendations.append({
            "title": "Sales Growth",
            "priority": "INFO",
            "action":
            f"Order {orders} ခု ရရှိထားပါသည်။ Customer Retention Strategy အသုံးပြုပါ"
        })



    # ==========================
    # PAYMENT
    # ==========================

    payments = (
        db.query(Payment)
        .filter(
            Payment.tenant_id == tenant_id
        )
        .count()
    )


    if payments == 0:

        recommendations.append({
            "title": "Payment Monitoring",
            "priority": "INFO",
            "action":
            "Payment Activity မရှိသေးပါ။ Finance Dashboard စောင့်ကြည့်ရန်လိုအပ်ပါသည်"
        })



    # ==========================
    # AI MEMORY SAVE
    # ==========================

    for item in recommendations:

        save_ai_memory(
            db,
            tenant_id,
            "AI_RECOMMENDATION",
            f"{item['title']}: {item['action']}"
        )


    return recommendations
