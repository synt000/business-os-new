from src.domains.payment.models import (
    PaymentMethod,
    TenantPaymentMethod,
)
from src.domains.payment.services.payment_config_service import get_available_payment_methods
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.domains.trial.guard import require_active_subscription
from src.models.saas_core import (
    User,
    Order,
    OrderItem,
    Invoice,
    Receivable,
    Customer,
)
from src.domains.product.models import Product
from src.domains.inventory.services.stock_service import restore_stock

from src.domains.order.schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)

from src.domains.order.services.order_service import create_order
from src.domains.invoice.schemas import InvoiceCreate
from src.domains.invoice.services.invoice_service import create_invoice

router = APIRouter(
    prefix="/api/v4/business/orders",
    tags=["Orders"]
)


@router.get("/")
async def list_orders(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == current_user.tenant_id
        )
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        {
            "id": o.id,
            "order_number": o.order_number,
            "status": o.order_status,
            "total_amount": o.total_amount,
            "created_at": o.created_at,
        }
        for o in orders
    ]


@router.post(
    "/",
    response_model=OrderResponse
)
async def create_new_order(
    data: OrderCreate,
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    try:

        order = create_order(
            db,
            current_user.tenant_id,
            data.order_number,
            data.items,
            data.customer_id,
            data.customer_name,
            data.customer_phone,
        )

        invoice_data = InvoiceCreate(
            order_id=order.id,
            invoice_number=f"INV-{order.order_number}"
        )

        create_invoice(
            db,
            current_user.tenant_id,
            invoice_data,
        )

        db.commit()
        db.refresh(order)

        return order

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/list")
async def get_orders(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):

    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == current_user.tenant_id
        )
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        {
            "id": o.id,
            "order_number": o.order_number,
            "status": o.order_status,
            "total_amount": o.total_amount,
            "created_at": o.created_at,
        }
        for o in orders
    ]


@router.get("/detail/{order_id}")
async def get_order_detail(
    order_id: str,
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="ORDER_NOT_FOUND"
        )

    items = []

    for item in order.items:

        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id,
                Product.tenant_id == current_user.tenant_id
            )
            .first()
        )

        items.append(
            {
                "product_id": item.product_id,
                "product_name": product.name if product else None,
                "quantity": item.quantity,
                "price": item.price_at_sale,
            }
        )

    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_id": order.customer_id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "status": order.order_status,
        "total_amount": order.total_amount,
        "items": items,
    }


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="ORDER_NOT_FOUND"
        )


    allowed = [
        "PENDING",
        "CONFIRMED",
        "PACKING",
        "SHIPPED",
        "COMPLETED",
        "CANCELLED"
    ]


    if data.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail="INVALID_STATUS"
        )


    old_status = order.order_status

    allowed_transitions = {
        "PENDING": {"CONFIRMED", "CANCELLED"},
        "CONFIRMED": {"PACKING", "CANCELLED"},
        "PACKING": {"SHIPPED", "CANCELLED"},
        "SHIPPED": {"COMPLETED", "CANCELLED"},
        "PAID": {"COMPLETED"},
        "COMPLETED": set(),
        "CANCELLED": set(),
    }

    if data.status not in allowed_transitions.get(old_status, set()):
        raise HTTPException(
            status_code=400,
            detail="INVALID_STATUS_TRANSITION"
        )


    if (
        data.status == "CANCELLED"
        and old_status in [
            "CONFIRMED",
            "PACKING",
            "SHIPPED"
        ]
    ):

        for item in order.items:

            product = (
                db.query(Product)
                .filter(
                    Product.id == item.product_id,
                    Product.tenant_id == current_user.tenant_id
                )
                .first()
            )

            if product:

                restore_stock(
                    db,
                    product,
                    item.quantity,
                    "Order Cancel"
                )


    order.order_status = data.status

    db.commit()
    db.refresh(order)

    return {
        "id": order.id,
        "status": order.order_status
    }


@router.put("/{order_id}/payment")
async def pay_order(
    order_id: str,
    payment_method: str,
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db),
):
    print("=== PAY ORDER LIVE ENTRY ===")
    print("ORDER_ID =", order_id)
    print("PAYMENT_METHOD RAW =", repr(payment_method))
    print("USER TENANT =", repr(current_user.tenant_id))



    print("RAW PAYMENT:", repr(payment_method))
    payment_method = payment_method.strip().upper()
    print("PAYMENT DEBUG:", repr(payment_method))
    print("PAYMENT ALLOWED CHECK:", payment_method in ["CASH","KBZPAY","WAVEPAY","KBZ_BANK","CB_BANK","CB_ATM","WAVE_MONEY","BANK"])

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="ORDER_NOT_FOUND"
        )

    print("DEBUG PAYMENT VALUE =", repr(payment_method), "TYPE=", type(payment_method))

    print("=== TENANT DEBUG ===")
    print("CURRENT USER TENANT =", repr(current_user.tenant_id))
    print("====================")

    print("===== PAYMENT TENANT CHECK =====")
    print("CURRENT USER ID =", repr(current_user.id))
    print("CURRENT TENANT ID =", repr(current_user.tenant_id))
    print("================================")

    allowed_methods = [
        row.code
        for row in (
            db.query(PaymentMethod.code)
            .join(
                TenantPaymentMethod,
                TenantPaymentMethod.payment_method_id == PaymentMethod.id
            )
            .filter(
                TenantPaymentMethod.tenant_id == current_user.tenant_id,
                TenantPaymentMethod.enabled == True,
                PaymentMethod.active == True
            )
            .all()
        )
    ]

    print("========== PAYMENT TRACE ==========")
    print("TENANT =", repr(current_user.tenant_id))
    print("PAYMENT VALUE =", repr(payment_method))
    print("PAYMENT TYPE =", type(payment_method))
    print("ALLOWED =", [repr(x) for x in allowed_methods])
    print("COMPARE RESULT =", payment_method in allowed_methods)
    print("===================================")

    if payment_method not in allowed_methods:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "INVALID_PAYMENT_METHOD",
                "received": repr(payment_method),
                "received_length": len(payment_method),
                "allowed": [repr(x) for x in allowed_methods],
                "tenant": repr(current_user.tenant_id)
            }
        )

    order.order_status = "PAID"

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.order_id == order.id,
            Invoice.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if invoice:
        invoice.status = "PAID"

        receivable = (
            db.query(Receivable)
            .filter(
                Receivable.invoice_id == invoice.id,
                Receivable.tenant_id == current_user.tenant_id
            )
            .first()
        )

        if receivable:
            receivable.paid_amount = receivable.total_amount
            receivable.balance_amount = 0
            receivable.status = "PAID"

    db.commit()
    db.refresh(order)

    return {
        "status": "PAYMENT_SUCCESS",
        "order_id": order.id,
        "order_number": order.order_number,
        "payment_method": payment_method,
        "order_status": order.order_status
    }



@router.put("/{order_id}/complete")
async def complete_order(
    order_id: str,
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="ORDER_NOT_FOUND"
        )

    if order.order_status != "PAID":
        raise HTTPException(
            status_code=400,
            detail="ONLY_PAID_ORDER_CAN_BE_COMPLETED"
        )

    order.order_status = "COMPLETED"

    db.commit()
    db.refresh(order)

    return {
        "status": "ORDER_COMPLETED",
        "order_id": order.id,
        "order_number": order.order_number,
        "order_status": order.order_status
    }
