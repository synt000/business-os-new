from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import (
    User,
    Employee,
)


router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)


@router.get("/employees")
def list_employees(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    employees = (
        db.query(Employee)
        .filter(
            Employee.tenant_id == current_user.tenant_id
        )
        .all()
    )

    return {
        "status": "SUCCESS",
        "count": len(employees),
        "employees": employees
    }


@router.post("/employees")
def create_employee(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    employee = Employee(
        id=str(uuid.uuid4()),
        employee_code=data.get(
            "employee_code"
        ),
        full_name=data.get(
            "full_name"
        ),
        phone=data.get(
            "phone"
        ),
        email=data.get(
            "email"
        ),
        department=data.get(
            "department"
        ),
        position=data.get(
            "position"
        ),
        salary=data.get(
            "salary",
            0
        ),
        tenant_id=current_user.tenant_id
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return {
        "status": "SUCCESS",
        "employee": employee
    }
