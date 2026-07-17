from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import Invoice
from src.models.business_profile import BusinessProfile

from src.domains.rental.models import (
    RentalItem,
    Rental,
    RentalCustomer,
    RentalDeposit,
    RentalMaintenance,
    RentalReturn,
)

from src.domains.rental.services.rental_service import (
    create_rental_payment,
)


router = APIRouter(
    prefix="/rental",
    tags=["Rental"]
)



@router.get("/customers")
def list_customers(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == current_user.tenant_id
        )
        .all()
    )


@router.post("/customers")
def create_customer(
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    customer = RentalCustomer(
        id=__import__("src.models.saas_core", fromlist=["generate_uuid"]).generate_uuid(),
        tenant_id=current_user.tenant_id,
        name=payload["name"],
        phone=payload.get("phone"),
        address=payload.get("address")
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get("/items")
def list_items(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(RentalItem)
        .filter(
            RentalItem.tenant_id == current_user.tenant_id
        )
        .all()
    )


@router.post("/items")
def create_item(
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    item = RentalItem(
        tenant_id=current_user.tenant_id,
        item_name=payload["item_name"],
        category=payload.get("category"),
        rate_per_hour=payload.get("rate_per_hour", 0),
        rate_per_day=payload.get("rate_per_day", 0)
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item



@router.get("/rentals")
def list_rentals(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(Rental)
        .filter(
            Rental.tenant_id == current_user.tenant_id
        )
        .all()
    )



@router.post("/rentals")
def create_rental(
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):


    # RENTAL AVAILABILITY CHECK
    new_start = datetime.fromisoformat(payload["start_time"])
    new_end = datetime.fromisoformat(payload["end_time"])

    conflict = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == current_user.tenant_id,
            Rental.item_id == payload["item_id"],
            Rental.rental_status.in_([
                "PENDING",
                "ACTIVE"
            ])
        )
        .all()
    )

    for existing in conflict:
        if existing.start_time < new_end and existing.end_time > new_start:
            raise HTTPException(
                status_code=400,
                detail="ITEM_ALREADY_RENTED_FOR_SELECTED_TIME"
            )

    if conflict:
        raise HTTPException(
            status_code=400,
            detail="ITEM_ALREADY_RENTED_FOR_SELECTED_TIME"
        )

    rental = Rental(
        tenant_id=current_user.tenant_id,
        customer_id=payload.get("customer_id"),
        item_id=payload["item_id"],
        start_time=datetime.fromisoformat(payload["start_time"]),
        end_time=datetime.fromisoformat(payload["end_time"]),
        total_amount=payload.get("total_amount", 0)
    )

    db.add(rental)

    # Update item status
    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == rental.item_id,
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if item:
        print("🔥 ITEM STATUS UPDATE RUNNING:", item.id)
        item.status = "RENTED"
        print("🔥 NEW STATUS:", item.status)

    db.commit()
    db.refresh(rental)

    return rental



@router.post("/payments")
def create_payment(
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        return create_rental_payment(
            db=db,
            tenant_id=current_user.tenant_id,
            rental_id=payload["rental_id"],
            amount=payload.get("amount_paid", 0),
            payment_method=payload.get("payment_method")
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/payments/{rental_id}")
def list_rental_payments(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.rental.models import RentalPayment

    payments = (
        db.query(RentalPayment)
        .filter(
            RentalPayment.rental_id == rental_id,
            RentalPayment.tenant_id == current_user.tenant_id
        )
        .all()
    )

    return payments


@router.get("/rentals/{rental_id}")
def get_rental_detail(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.rental.models import RentalPayment, RentalItem

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="RENTAL_NOT_FOUND"
        )


    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == rental.item_id,
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )

    customer = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.id == rental.customer_id,
            RentalCustomer.tenant_id == current_user.tenant_id
        )
        .first()
    )


    paid_amount = (
        db.query(RentalPayment)
        .filter(
            RentalPayment.rental_id == rental_id,
            RentalPayment.tenant_id == current_user.tenant_id
        )
        .with_entities(
            __import__("sqlalchemy").func.sum(
                RentalPayment.amount_paid
            )
        )
        .scalar()
        or 0
    )


    balance = rental.total_amount - paid_amount


    now = datetime.utcnow()

    if balance <= 0:
        rental_status = "PAID"
    elif now < rental.start_time:
        rental_status = "PENDING"
    elif now >= rental.start_time and now <= rental.end_time:
        rental_status = "ACTIVE"
    else:
        rental_status = "COMPLETED"



    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "rental_id": rental.id,
        "item_name": item.item_name if item else None,
        "category": item.category if item else None,
        "start_time": rental.start_time,
        "end_time": rental.end_time,
        "total_amount": rental.total_amount,
        "paid_amount": paid_amount,
        "balance": balance,
        "status": rental_status,
        "customer_id": rental.customer_id,

        "customer": {
            "id": customer.id if customer else None,
            "name": customer.name if customer else None,
            "phone": customer.phone if customer else None,
            "address": customer.address if customer else None
        },

        "tenant_id": rental.tenant_id
    }



@router.post("/deposits")
def create_deposit(
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    deposit = RentalDeposit(
        tenant_id=current_user.tenant_id,
        rental_id=payload["rental_id"],
        amount=payload.get("amount", 0)
    )

    db.add(deposit)
    db.commit()
    db.refresh(deposit)

    return deposit


@router.get("/deposits/{rental_id}")
def get_deposit(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(RentalDeposit)
        .filter(
            RentalDeposit.tenant_id == current_user.tenant_id,
            RentalDeposit.rental_id == rental_id
        )
        .all()
    )

@router.post("/deposits/{deposit_id}/refund")
def refund_deposit(
    deposit_id: str,
    payload: dict,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deposit = (
        db.query(RentalDeposit)
        .filter(
            RentalDeposit.id == deposit_id,
            RentalDeposit.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if not deposit:
        raise HTTPException(
            status_code=404,
            detail="DEPOSIT_NOT_FOUND"
        )

    deposit.status = "REFUNDED"
    deposit.refund_amount = payload.get("refund_amount", 0)

    db.commit()
    db.refresh(deposit)

    return deposit



@router.post("/returns/{rental_id}")
def create_return(
    rental_id: str,
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="RENTAL_NOT_FOUND"
        )


    return_record = RentalReturn(
        tenant_id=current_user.tenant_id,
        rental_id=rental_id,
        condition=payload.get("condition", "GOOD"),
        damage_amount=payload.get("damage_amount", 0)
    )


    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == rental.item_id,
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if item:
        item.status = "AVAILABLE"


    rental.rental_status = "COMPLETED"


    # Deposit Settlement

    deposit = (
        db.query(RentalDeposit)
        .filter(
            RentalDeposit.rental_id == rental_id,
            RentalDeposit.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if deposit:

        damage = payload.get("damage_amount", 0)

        refund = deposit.amount - damage

        if refund < 0:
            refund = 0

        deposit.refund_amount = refund

        if damage > 0:
            deposit.status = "PARTIAL_REFUND"
        else:
            deposit.status = "REFUNDED"


    db.add(return_record)

    rental.rental_status = "COMPLETED"

    if item:
        item.status = "AVAILABLE"


    db.commit()
    db.refresh(return_record)

    return return_record


@router.get("/dashboard/summary")
def rental_dashboard_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from sqlalchemy import func
    from src.domains.rental.models import (
        RentalItem,
        Rental,
        RentalDeposit,
        RentalPayment,
        RentalReturn
    )

    tenant_id = current_user.tenant_id


    total_items = (
        db.query(RentalItem)
        .filter(
            RentalItem.tenant_id == tenant_id
        )
        .count()
    )


    available_items = (
        db.query(RentalItem)
        .filter(
            RentalItem.tenant_id == tenant_id,
            RentalItem.status == "AVAILABLE"
        )
        .count()
    )


    active_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status.in_(
                [
                    "PENDING",
                    "ACTIVE"
                ]
            )
        )
        .count()
    )


    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(RentalPayment.amount_paid),
                0
            )
        )
        .filter(
            RentalPayment.tenant_id == tenant_id
        )
        .scalar()
    )


    held_deposit = (
        db.query(
            func.coalesce(
                func.sum(RentalDeposit.amount),
                0
            )
        )
        .filter(
            RentalDeposit.tenant_id == tenant_id,
            RentalDeposit.status.in_(
                [
                    "HELD",
                    "PARTIAL_REFUND"
                ]
            )
        )
        .scalar()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )



    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "status": "SUCCESS",
        "dashboard": {
            "total_items": total_items,
            "available_items": available_items,
            "active_rentals": active_rentals,
            "total_revenue": total_revenue,
            "held_deposit": held_deposit,
            "damage_fee": damage_fee,
            "completed_rentals": completed_rentals,
            "total_customers": total_customers,
            "maintenance_cost": maintenance_cost,
            "net_profit": net_profit
        }
    }



@router.post("/status/update")
def update_rental_status(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from datetime import datetime

    rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == current_user.tenant_id
        )
        .all()
    )

    now = datetime.utcnow()

    updated = []

    for rental in rentals:

        if now < rental.start_time:
            rental.rental_status = "PENDING"

        elif rental.start_time <= now <= rental.end_time:
            rental.rental_status = "ACTIVE"

        else:
            rental.rental_status = "COMPLETED"

        updated.append({
            "id": rental.id,
            "status": rental.rental_status
        })

    db.commit()


    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "status": "SUCCESS",
        "updated": updated
    }



@router.post("/maintenance")
def create_maintenance(
    payload: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    maintenance = RentalMaintenance(
        tenant_id=current_user.tenant_id,
        item_id=payload["item_id"],
        rental_id=payload.get("rental_id"),
        issue=payload.get("issue", "UNKNOWN"),
        repair_cost=payload.get("repair_cost", 0)
    )

    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == payload["item_id"],
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if item:
        item.status = "MAINTENANCE"

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return maintenance



@router.get("/maintenance")
def list_maintenance(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(RentalMaintenance)
        .filter(
            RentalMaintenance.tenant_id == current_user.tenant_id
        )
        .all()
    )



@router.put("/maintenance/{maintenance_id}/complete")
def complete_maintenance(
    maintenance_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    maintenance = (
        db.query(RentalMaintenance)
        .filter(
            RentalMaintenance.id == maintenance_id,
            RentalMaintenance.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="MAINTENANCE_NOT_FOUND"
        )


    maintenance.status = "COMPLETED"
    maintenance.completed_at = datetime.utcnow()


    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == maintenance.item_id,
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if item:
        item.status = "AVAILABLE"


    db.commit()
    db.refresh(maintenance)

    return maintenance



@router.get("/settlement/{rental_id}")
def rental_settlement(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.rental.models import (
        RentalPayment,
        RentalDeposit,
        RentalReturn,
        RentalMaintenance
    )

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="RENTAL_NOT_FOUND"
        )


    paid_amount = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalPayment.amount_paid
        ))
        .filter(
            RentalPayment.rental_id == rental_id,
            RentalPayment.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    deposit_amount = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalDeposit.amount
        ))
        .filter(
            RentalDeposit.rental_id == rental_id,
            RentalDeposit.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    refund_amount = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalDeposit.refund_amount
        ))
        .filter(
            RentalDeposit.rental_id == rental_id,
            RentalDeposit.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    damage_fee = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalReturn.damage_amount
        ))
        .filter(
            RentalReturn.rental_id == rental_id,
            RentalReturn.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    maintenance_cost = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalMaintenance.repair_cost
        ))
        .filter(
            RentalMaintenance.rental_id == rental_id,
            RentalMaintenance.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    customer_refund = (
        deposit_amount
        - damage_fee
        - maintenance_cost
    )

    if customer_refund < 0:
        customer_refund = 0


    net_profit = (
        rental.total_amount
        - maintenance_cost
    )



    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "status": "SUCCESS",
        "settlement": {
            "rental_id": rental.id,
            "rental_amount": rental.total_amount,
            "paid_amount": paid_amount,
            "deposit_amount": deposit_amount,
            "deposit_refunded": refund_amount,
            "damage_fee": damage_fee,
            "maintenance_cost": maintenance_cost,
            "customer_refund_due": customer_refund,
            "net_profit": net_profit
        }
    }



@router.put("/settlement/{rental_id}/close")
def close_rental_settlement(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.rental.models import (
        RentalItem,
        RentalDeposit
    )

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="RENTAL_NOT_FOUND"
        )


    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == rental.item_id,
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )


    # Close rental
    rental.rental_status = "COMPLETED"


    # Release item
    if item:
        item.status = "AVAILABLE"


    # Close deposits
    deposits = (
        db.query(RentalDeposit)
        .filter(
            RentalDeposit.rental_id == rental_id,
            RentalDeposit.tenant_id == current_user.tenant_id
        )
        .all()
    )

    for deposit in deposits:
        deposit.status = "SETTLED"


    db.commit()
    db.refresh(rental)



    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "status": "SUCCESS",
        "message": "RENTAL_SETTLEMENT_CLOSED",
        "rental_id": rental.id,
        "rental_status": rental.rental_status,
        "item_status": item.status if item else None
    }



@router.get("/invoice/{rental_id}")
def rental_invoice(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.rental.models import (
        RentalPayment,
        RentalDeposit,
        RentalReturn,
        RentalMaintenance,
        RentalItem,
        RentalCustomer
    )

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="RENTAL_NOT_FOUND"
        )


    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == rental.item_id
        )
        .first()
    )


    customer = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.id == rental.customer_id
        )
        .first()
    )


    paid = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalPayment.amount_paid
        ))
        .filter(
            RentalPayment.rental_id == rental_id
        )
        .scalar()
        or 0
    )


    deposit = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalDeposit.amount
        ))
        .filter(
            RentalDeposit.rental_id == rental_id
        )
        .scalar()
        or 0
    )


    damage = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalReturn.damage_amount
        ))
        .filter(
            RentalReturn.rental_id == rental_id
        )
        .scalar()
        or 0
    )


    maintenance = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalMaintenance.repair_cost
        ))
        .filter(
            RentalMaintenance.rental_id == rental_id
        )
        .scalar()
        or 0
    )



    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "status": "SUCCESS",
        "invoice": {
            "invoice_id": f"RENTAL-{rental.id[:8]}",
            "customer": {
                "name": customer.name if customer else None,
                "phone": customer.phone if customer else None
            },
            "item": {
                "name": item.item_name if item else None,
                "category": item.category if item else None
            },
            "rental_period": {
                "start": rental.start_time,
                "end": rental.end_time
            },
            "financial": {
                "rental_amount": rental.total_amount,
                "paid_amount": paid,
                "deposit": deposit,
                "damage_fee": damage,
                "maintenance_cost": maintenance,
                "final_status": rental.rental_status
            }
        }
    }



@router.get("/history")
def rental_history(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.rental.models import (
        RentalPayment,
        RentalReturn,
        RentalMaintenance,
        RentalCustomer,
    )

    rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == current_user.tenant_id
        )
        .all()
    )


    completed = [
        r for r in rentals
        if r.rental_status == "COMPLETED"
    ]


    total_revenue = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalPayment.amount_paid
        ))
        .filter(
            RentalPayment.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    damage_fee = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalReturn.damage_amount
        ))
        .filter(
            RentalReturn.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    maintenance_cost = (
        db.query(__import__("sqlalchemy").func.sum(
            RentalMaintenance.repair_cost
        ))
        .filter(
            RentalMaintenance.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )


    customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == current_user.tenant_id
        )
        .count()
    )



    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )


    total_customers = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.tenant_id == tenant_id
        )
        .count()
    )


    damage_fee = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )


    maintenance_cost = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )


    net_profit = total_revenue - maintenance_cost

    return {
        "status": "SUCCESS",
        "history": {
            "completed_rentals": len(completed),
            "total_revenue": total_revenue,
            "damage_fee": damage_fee,
            "maintenance_cost": maintenance_cost,
            "net_profit": total_revenue - maintenance_cost,
            "total_customers": customers,
            "rentals": [
                {
                    "id": r.id,
                    "status": r.rental_status,
                    "amount": r.total_amount,
                    "start_time": r.start_time,
                    "end_time": r.end_time
                }
                for r in rentals
            ]
        }
    }





@router.get("/invoice/{rental_id}/pdf")
def export_invoice_pdf(
    rental_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from io import BytesIO
    from sqlalchemy import func

    from src.domains.rental.models import (
        RentalPayment,
        RentalDeposit,
        RentalReturn,
        RentalMaintenance
    )

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="RENTAL_NOT_FOUND"
        )

    item = (
        db.query(RentalItem)
        .filter(
            RentalItem.id == rental.item_id,
            RentalItem.tenant_id == current_user.tenant_id
        )
        .first()
    )

    customer = (
        db.query(RentalCustomer)
        .filter(
            RentalCustomer.id == rental.customer_id,
            RentalCustomer.tenant_id == current_user.tenant_id
        )
        .first()
    )

    business = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.tenant_id == current_user.tenant_id
        )
        .first()
    )

    paid_amount = (
        db.query(func.sum(RentalPayment.amount_paid))
        .filter(
            RentalPayment.rental_id == rental_id,
            RentalPayment.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )

    deposit_amount = (
        db.query(func.sum(RentalDeposit.amount))
        .filter(
            RentalDeposit.rental_id == rental_id,
            RentalDeposit.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )

    deposit_refunded = (
        db.query(func.sum(RentalDeposit.refund_amount))
        .filter(
            RentalDeposit.rental_id == rental_id,
            RentalDeposit.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )

    damage_fee = (
        db.query(func.sum(RentalReturn.damage_amount))
        .filter(
            RentalReturn.rental_id == rental_id,
            RentalReturn.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )

    maintenance_cost = (
        db.query(func.sum(RentalMaintenance.repair_cost))
        .filter(
            RentalMaintenance.rental_id == rental_id,
            RentalMaintenance.tenant_id == current_user.tenant_id
        )
        .scalar()
        or 0
    )

    customer_refund = deposit_amount - damage_fee - maintenance_cost

    if customer_refund < 0:
        customer_refund = 0

    net_profit = rental.total_amount - maintenance_cost


    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    def add_footer(canvas, doc):
        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8
        )

        canvas.drawString(
            40,
            20,
            "Business OS Enterprise"
        )

        canvas.drawRightString(
            550,
            20,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            f"{business.business_name if business else 'BUSINESS OS'} - RENTAL INVOICE",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))


    data = [
        ["Invoice ID", f"RENTAL-{rental.id[:8]}"],
        ["Customer", customer.name if customer else ""],
        ["Phone", customer.phone if customer else ""],
        ["Item", item.item_name if item else ""],
        ["Category", item.category if item else ""],
        ["Start", str(rental.start_time)],
        ["End", str(rental.end_time)],
        ["Rental Amount", str(rental.total_amount)],
        ["Paid Amount", str(paid_amount)],
        ["Deposit", str(deposit_amount)],
        ["Deposit Refunded", str(deposit_refunded)],
        ["Damage Fee", str(damage_fee)],
        ["Maintenance Cost", str(maintenance_cost)],
        ["Customer Refund Due", str(customer_refund)],
        ["Net Profit", str(net_profit)],
        ["Status", rental.rental_status],
    ]


    table = Table(data)

    table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,None),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ])
    )

    elements.append(table)

    # Enterprise KPI Cards

    kpi_data = [
        [
            Paragraph(
                f"<b>Total Items</b><br/>{total_items}",
                styles["Normal"]
            ),
            Paragraph(
                f"<b>Available</b><br/>{available_items}",
                styles["Normal"]
            ),
            Paragraph(
                f"<b>Revenue</b><br/>{revenue:,.0f}",
                styles["Normal"]
            ),
            Paragraph(
                f"<b>Net Profit</b><br/>{net_profit:,.0f}",
                styles["Normal"]
            ),
        ]
    ]

    kpi_table = Table(
        kpi_data,
        colWidths=[100,100,100,100]
    )

    kpi_table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#d1d5db")),
            ("BACKGROUND",(0,0),(0,0),colors.HexColor("#e0f2fe")),
            ("BACKGROUND",(1,0),(1,0),colors.HexColor("#dcfce7")),
            ("BACKGROUND",(2,0),(2,0),colors.HexColor("#fef3c7")),
            ("BACKGROUND",(3,0),(3,0),colors.HexColor("#ede9fe")),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("TOPPADDING",(0,0),(-1,-1),12),
            ("BOTTOMPADDING",(0,0),(-1,-1),12),
        ])
    )

    elements.append(
        Spacer(1,20)
    )

    elements.append(kpi_table)


    elements.append(
        Spacer(1,20)
    )

    summary_data = [
        [
            Paragraph(
                f"<b>Profit Margin</b><br/>{profit_margin:.1f}%",
                styles["Normal"]
            ),
            Paragraph(
                f"<b>Occupancy Rate</b><br/>{occupancy_rate:.1f}%",
                styles["Normal"]
            ),
            Paragraph(
                f"<font color='{'green' if business_health == 'GOOD' else 'red'}'><b>Business Health</b><br/>{business_health}</font>",
                styles["Normal"]
            ),
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[130,130,130]
    )

    summary_table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#9ca3af")),
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f1f5f9")),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),12),
            ("BOTTOMPADDING",(0,0),(-1,-1),12),
        ])
    )

    elements.append(summary_table)



    elements.append(Spacer(1,40))

    elements.append(
        Paragraph(
            "Customer Signature ____________________",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "Staff Signature ____________________",
            styles["Normal"]
        )
    )


    doc.build(elements)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f"attachment; filename=invoice_{rental.id}.pdf"
        }
    )


@router.get("/dashboard/report/pdf")
def rental_dashboard_report_pdf(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from io import BytesIO
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from sqlalchemy import func
    from src.models.business_profile import BusinessProfile
    from src.domains.rental.models import (
        RentalPayment,
        RentalMaintenance,
        RentalReturn
    )

    tenant_id = current_user.tenant_id

    business = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.tenant_id == tenant_id
        )
        .first()
    )

    total_items = (
        db.query(RentalItem)
        .filter(RentalItem.tenant_id == tenant_id)
        .count()
    )

    available_items = (
        db.query(RentalItem)
        .filter(
            RentalItem.tenant_id == tenant_id,
            RentalItem.status == "AVAILABLE"
        )
        .count()
    )

    completed_rentals = (
        db.query(Rental)
        .filter(
            Rental.tenant_id == tenant_id,
            Rental.rental_status == "COMPLETED"
        )
        .count()
    )

    revenue = (
        db.query(
            func.coalesce(
                func.sum(RentalPayment.amount_paid),
                0
            )
        )
        .filter(
            RentalPayment.tenant_id == tenant_id
        )
        .scalar()
    )

    maintenance = (
        db.query(
            func.coalesce(
                func.sum(RentalMaintenance.repair_cost),
                0
            )
        )
        .filter(
            RentalMaintenance.tenant_id == tenant_id
        )
        .scalar()
    )

    damage = (
        db.query(
            func.coalesce(
                func.sum(RentalReturn.damage_amount),
                0
            )
        )
        .filter(
            RentalReturn.tenant_id == tenant_id
        )
        .scalar()
    )

    net_profit = revenue - maintenance

    profit_margin = (
        (net_profit / revenue * 100)
        if revenue > 0
        else 0
    )

    occupancy_rate = (
        ((total_items - available_items) / total_items * 100)
        if total_items > 0
        else 0
    )

    business_health = (
        "GOOD"
        if profit_margin >= 50
        else "WARNING"
    )

    health_color = (
        colors.HexColor("#16a34a")
        if business_health == "GOOD"
        else colors.HexColor("#dc2626")
    )

    monthly_revenue = (
        db.query(
            func.strftime('%Y-%m', RentalPayment.paid_at),
            func.sum(RentalPayment.amount_paid)
        )
        .filter(
            RentalPayment.tenant_id == tenant_id
        )
        .group_by(
            func.strftime('%Y-%m', RentalPayment.paid_at)
        )
        .order_by(
            func.strftime('%Y-%m', RentalPayment.paid_at)
        )
        .all()
    )

    best_month = (
        max(
            monthly_revenue,
            key=lambda x: x[1] or 0
        )
        if monthly_revenue
        else None
    )

    best_month_label = (
        best_month[0]
        if best_month
        else "-"
    )

    best_month_amount = (
        best_month[1]
        if best_month
        else 0
    )

    previous_revenue = 0
    current_revenue = 0
    revenue_growth = 0

    if len(monthly_revenue) >= 2:
        previous_revenue = monthly_revenue[-2][1] or 0
        current_revenue = monthly_revenue[-1][1] or 0

        if previous_revenue > 0:
            revenue_growth = (
                (current_revenue - previous_revenue)
                / previous_revenue
                * 100
            )

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    company_name = (
        business.business_name
        if business
        else "BUSINESS OS"
    )

    logo_url = (
        business.logo_url
        if business and business.logo_url
        else None
    )

    company_phone = (
        business.phone
        if business and business.phone
        else "-"
    )

    generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    header_data = []

    header_text = [
        Paragraph(
            company_name,
            styles["Title"]
        ),
        Paragraph(
            "Rental Dashboard Report",
            styles["Heading2"]
        ),
        Paragraph(
            f"Phone: {company_phone}",
            styles["Normal"]
        ),
        Paragraph(
            f"Generated: {generated_date}",
            styles["Normal"]
        )
    ]

    if logo_url:
        try:
            logo = Image(
                logo_url,
                width=80,
                height=80
            )
            header_data.append([logo, header_text])
        except Exception:
            header_data.append(["", header_text])
    else:
        header_data.append(["", header_text])

    header_table = Table(
        header_data,
        colWidths=[100, 350]
    )

    header_table.setStyle(
        TableStyle([
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("LEFTPADDING",(0,0),(-1,-1),12),
            ("RIGHTPADDING",(0,0),(-1,-1),12),
            ("TOPPADDING",(0,0),(-1,-1),12),
            ("BOTTOMPADDING",(0,0),(-1,-1),12),
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#eff6ff")),
            ("BOX",(0,0),(-1,-1),1,colors.HexColor("#2563eb")),
            ("LINEBELOW",(0,0),(-1,-1),0.5,colors.HexColor("#93c5fd")),
        ])
    )

    elements.append(header_table)
    elements.append(Spacer(1,20))

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Rental Dashboard Report",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1,20))

    data = [
        ["Metric","Value"],
        ["Total Items", str(total_items)],
        ["Available Items", str(available_items)],
        ["Completed Rentals", str(completed_rentals)],
        ["Revenue", str(revenue)],
        ["Damage Fee", str(damage)],
        ["Maintenance Cost", str(maintenance)],
        ["Net Profit", str(net_profit)],
    ]

    table = Table(
        data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,None),
            ("BACKGROUND",(0,0),(-1,0),"#1f2937"),
            ("TEXTCOLOR",(0,0),(-1,0),"white"),
            ("ALIGN",(1,1),(-1,-1),"RIGHT"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),8),
            ("RIGHTPADDING",(0,0),(-1,-1),8),
            ("TOPPADDING",(0,0),(-1,-1),6),
            ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1,15)
    )

    profit_box = Table(
        [
            ["NET PROFIT", f"{net_profit:,.0f}"]
        ],
        colWidths=[150,150]
    )

    profit_box.setStyle(
        TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#065f46")),
            ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("GRID",(0,0),(-1,-1),0.5,colors.white),
            ("TOPPADDING",(0,0),(-1,-1),10),
            ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ])
    )

    elements.append(profit_box)

    elements.append(
        Spacer(1,30)
    )

    elements.append(
        Paragraph(
            "Financial Analytics Summary",
            styles["Heading2"]
        )
    )

    analytics_data = [
        ["Category","Amount"],
        ["Revenue", f"{revenue:,.0f}"],
        ["Damage Fee", f"{damage:,.0f}"],
        ["Maintenance Cost", f"{maintenance:,.0f}"],
        ["Net Profit", f"{net_profit:,.0f}"],
    ]

    analytics_table = Table(
        analytics_data,
        repeatRows=1
    )

    analytics_table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,None),
            ("BACKGROUND",(0,0),(-1,0),"#111827"),
            ("TEXTCOLOR",(0,0),(-1,0),"white"),
            ("ALIGN",(1,1),(-1,-1),"RIGHT"),
        ])
    )

    elements.append(analytics_table)

    elements.append(
        Paragraph(
            "Revenue vs Cost Analytics",
            styles["Heading2"]
        )
    )

    drawing = Drawing(400, 200)

    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 35
    chart.width = 300
    chart.height = 130

    chart.data = [[
        revenue,
        maintenance,
        damage,
        net_profit
    ]]

    chart.categoryAxis.categoryNames = [
        "Revenue",
        "Maintenance",
        "Damage",
        "Profit"
    ]

    chart.bars[0].fillColor = colors.HexColor("#2563eb")

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max(
        revenue,
        maintenance,
        damage,
        net_profit
    ) * 1.2

    chart.valueAxis.valueStep = max(
        1,
        int(
            max(
                revenue,
                maintenance,
                damage,
                net_profit
            ) / 5
        )
    )

    drawing.add(chart)

    elements.append(
        Spacer(1,20)
    )

    elements.append(
        Paragraph(
            "Monthly Revenue Trend",
            styles["Heading2"]
        )
    )

    monthly_drawing = Drawing(400,200)

    monthly_chart = VerticalBarChart()
    monthly_chart.x = 50
    monthly_chart.y = 35
    monthly_chart.width = 300
    monthly_chart.height = 130

    monthly_values = [
        float(item[1] or 0)
        for item in monthly_revenue
    ]

    if monthly_values:
        monthly_chart.data = [monthly_values]

        monthly_chart.categoryAxis.categoryNames = [
            item[0]
            for item in monthly_revenue
        ]

        monthly_chart.bars[0].fillColor = colors.HexColor("#16a34a")

        monthly_drawing.add(monthly_chart)

        elements.append(monthly_drawing)

        # Monthly Revenue Line Trend
        line_drawing = Drawing(400,200)

        line_chart = LineChart()
        line_chart.x = 50
        line_chart.y = 40
        line_chart.width = 300
        line_chart.height = 120

        line_chart.data = [monthly_values]

        line_chart.categoryAxis.categoryNames = [
            item[0]
            for item in monthly_revenue
        ]

        line_chart.lines[0].strokeColor = colors.HexColor("#16a34a")
        line_chart.lines[0].strokeWidth = 2

        line_chart.joinedLines = 1

        line_chart.lines[0].strokeColor = colors.HexColor("#2563eb")

        line_drawing.add(line_chart)

        elements.append(
            Spacer(1,20)
        )

        elements.append(
            Paragraph(
                "Monthly Revenue Line Trend",
                styles["Heading2"]
            )
        )

        elements.append(line_drawing)

        elements.append(
            Spacer(1,20)
        )

    elements.append(drawing)

    elements.append(
        Spacer(1,20)
    )

    elements.append(
        Paragraph(
            "Generated by Business OS Enterprise",
            styles["Normal"]
        )
    )

    doc.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=rental_dashboard_report.pdf"
        }
    )
