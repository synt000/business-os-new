from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import Customer
from .schemas import (
    CustomerCreate,
    CustomerResponse,
    AddressCreate,
    AddressResponse,
)
from .service import CustomerService

from .contracts.address_contract import AddressContext
from .services.address_service import CustomerAddressService


router = APIRouter(
    prefix="/api/v4/customers",
    tags=["Customers"]
)


@router.get(
    "",
    response_model=list[CustomerResponse]
)
def list_customers(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return CustomerService.list(
        db,
        tenant_id=current_user.tenant_id
    )


@router.post(
    "",
    response_model=CustomerResponse
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return CustomerService.create(
        db,
        tenant_id=current_user.tenant_id,
        payload=payload
    )


@router.get(
    "/ui",
    response_class=HTMLResponse
)
def customer_ui(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customers = CustomerService.list(
        db,
        tenant_id=current_user.tenant_id
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return CustomerService.get(
        db,
        customer_id=customer_id,
        tenant_id=current_user.tenant_id
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: str,
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return CustomerService.update(
        db,
        customer_id=customer_id,
        tenant_id=current_user.tenant_id,
        payload=payload
    )


@router.delete(
    "/{customer_id}"
)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return CustomerService.delete(
        db,
        customer_id=customer_id,
        tenant_id=current_user.tenant_id
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    customer = CustomerService.get(
        db,
        customer_id,
        tenant_id=current_user.tenant_id
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return CustomerService.analytics(
        db,
        customer_id,
        tenant_id=current_user.tenant_id
    )



@router.get(
    "/{customer_id}/orders"
)
def customer_orders(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return CustomerService.orders(
        db,
        customer_id,
        tenant_id=current_user.tenant_id
    )



@router.get(
    "/{customer_id}/revenue"
)
def customer_revenue(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return CustomerService.revenue(
        db,
        customer_id,
        tenant_id=current_user.tenant_id
    )



@router.post(
    "/{customer_id}/addresses",
    response_model=AddressResponse,
)
def create_customer_address(
    customer_id: str,
    payload: AddressCreate,
    db: Session = Depends(get_db),
):
    context = AddressContext(
        customer_id=customer_id,
        address_type=payload.address_type,
        line1=payload.line1,
        city=payload.city,
        township=payload.township,
        phone=payload.phone,
    )

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        return None

    return CustomerAddressService.create_address(
        db,
        tenant_id=customer.tenant_id,
        context=context,
    )


@router.get(
    "/{customer_id}/addresses",
    response_model=list[AddressResponse],
)
def get_customer_addresses(
    customer_id: str,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        return []

    return CustomerAddressService.get_customer_addresses(
        db,
        customer_id=customer_id,
        tenant_id=customer.tenant_id,
    )


@router.delete(
    "/{customer_id}/addresses/{address_id}",
)
def delete_customer_address(
    customer_id: str,
    address_id: str,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        return None

    return CustomerAddressService.delete_address(
        db,
        address_id=address_id,
        tenant_id=customer.tenant_id,
    )
