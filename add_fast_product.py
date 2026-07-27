from pathlib import Path

p = Path("src/domains/dashboard/service.py")
s = p.read_text()

code = '''

def get_fast_moving_product(
    db: Session,
    tenant_id: str
):
    product = (
        db.query(
            Product.name,
            func.sum(OrderItem.quantity).label("qty")
        )
        .join(
            OrderItem,
            OrderItem.product_id == Product.id
        )
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Product.tenant_id == tenant_id
        )
        .group_by(
            Product.id
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .first()
    )

    if not product:
        return {}

    return {
        "name": product.name,
        "units_sold": product.qty
    }
'''

if "def get_fast_moving_product" not in s:
    p.write_text(s + code)
    print("FAST PRODUCT FUNCTION ADDED")
else:
    print("ALREADY EXISTS")
