from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.core.database import get_db
from .schemas import CustomerCreate, CustomerResponse
from .service import CustomerService


router = APIRouter(
    prefix="/api/v4/customers",
    tags=["Customers"]
)


@router.get(
    "",
    response_model=list[CustomerResponse]
)
def list_customers(
    db: Session = Depends(get_db)
):

    return CustomerService.list(
        db,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )


@router.post(
    "",
    response_model=CustomerResponse
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db)
):

    return CustomerService.create(
        db,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d",
        payload=payload
    )


@router.get(
    "/ui",
    response_class=HTMLResponse
)
def customer_ui(
    request: Request,
    db: Session = Depends(get_db)
):
    customers = CustomerService.list(
        db,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )

    return templates.TemplateResponse(
        "customers.html",
        {
            "request": request,
            "customers": customers
        }
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return CustomerService.get(
        db,
        customer_id=customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: str,
    payload: CustomerCreate,
    db: Session = Depends(get_db)
):
    return CustomerService.update(
        db,
        customer_id=customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d",
        payload=payload
    )


@router.delete(
    "/{customer_id}"
)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return CustomerService.delete(
        db,
        customer_id=customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(
    directory="src/templates"
)




@router.get(
    "/{customer_id}/ui",
    response_class=HTMLResponse
)
def customer_profile_ui(
    request: Request,
    customer_id: str,
    db: Session = Depends(get_db)
):

    customer = CustomerService.get(
        db,
        customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )

    return templates.TemplateResponse(
        "customer_profile.html",
        {
            "request": request,
            "customer": customer
        }
    )


@router.get(
    "/{customer_id}/analytics"
)
def customer_analytics(
    customer_id: str,
    db: Session = Depends(get_db)
):

    return CustomerService.analytics(
        db,
        customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )



@router.get(
    "/{customer_id}/orders"
)
def customer_orders(
    customer_id: str,
    db: Session = Depends(get_db)
):

    return CustomerService.orders(
        db,
        customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )



@router.get(
    "/{customer_id}/revenue"
)
def customer_revenue(
    customer_id: str,
    db: Session = Depends(get_db)
):

    return CustomerService.revenue(
        db,
        customer_id,
        tenant_id="0d3a21e3-7356-440f-bdb8-e5598516935d"
    )

