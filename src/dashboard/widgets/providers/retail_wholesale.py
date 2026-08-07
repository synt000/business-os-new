from sqlalchemy import func

from src.models.saas_core import Order, OrderItem
from src.domains.product.models import Product
from src.domains.inventory.models import Inventory


def total_sales_widget(db, tenant_id):
    total = (
        db.query(func.sum(Order.total_amount))
        .filter(Order.tenant_id == tenant_id)
        .scalar()
    ) or 0

    return {
        "sales": float(total),
        "currency": "MMK",
    }


def gross_profit_widget(db, tenant_id):
    revenue = (
        db.query(func.sum(Order.total_amount))
        .filter(Order.tenant_id == tenant_id)
        .scalar()
    ) or 0

    cost = (
        db.query(
            func.sum(
                OrderItem.quantity * Product.purchase_price
            )
        )
        .join(
            Product,
            Product.id == OrderItem.product_id
        )
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Order.tenant_id == tenant_id
        )
        .scalar()
    ) or 0

    return {
        "profit": float(revenue - cost),
        "revenue": float(revenue),
        "cost": float(cost),
        "currency": "MMK",
    }


def retail_wholesale_ratio_widget(db, tenant_id):
    return {
        "retail": 0,
        "wholesale": 0,
    }


def average_ticket_widget(db, tenant_id):
    return {
        "average": 0,
        "currency": "MMK",
    }


def inventory_value_widget(db, tenant_id):
    value = (
        db.query(
            func.sum(
                Inventory.quantity *
                Product.purchase_price
            )
        )
        .join(
            Product,
            Product.id == Inventory.product_id
        )
        .filter(
            Product.tenant_id == tenant_id
        )
        .scalar()
    ) or 0

    return {
        "value": float(value),
        "currency": "MMK",
    }


def wholesale_ledger_widget(db, tenant_id):
    return {"entries": []}


def customer_credit_widget(db, tenant_id):
    return {"amount": 0, "currency": "MMK"}


def supplier_debt_widget(db, tenant_id):
    return {"amount": 0, "currency": "MMK"}


def purchase_orders_widget(db, tenant_id):
    return {"orders": []}


def b2b_billing_widget(db, tenant_id):
    return {"invoices": []}


def retail_pos_widget(db, tenant_id):
    return {"status": "READY"}


def bulk_price_widget(db, tenant_id):
    return {"prices": []}


def stock_in_grn_widget(db, tenant_id):
    return {"receipts": []}
