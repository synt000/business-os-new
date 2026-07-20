from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import Customer


def find_customer_match(
    db: Session,
    tenant_id: str,
    customer_name: str | None = None,
    customer_phone: str | None = None,
):
    """
    Social CRM Matcher Engine

    Priority:
    1. Exact phone
    2. Normalized phone
    3. Case insensitive name
    4. Partial name similarity

    Tenant isolation enforced.
    """

    base_query = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
        )
    )


    # 1. PHONE MATCH
    if customer_phone:

        customer = (
            base_query
            .filter(
                Customer.customer_phone == customer_phone
            )
            .first()
        )

        if customer:
            return customer


    # 2. NAME MATCH
    if customer_name:

        normalized = customer_name.strip().lower()

        customer = (
            base_query
            .filter(
                func.lower(
                    Customer.customer_name
                ) == normalized
            )
            .first()
        )

        if customer:
            return customer


        # 3. PARTIAL MATCH
        customer = (
            base_query
            .filter(
                func.lower(
                    Customer.customer_name
                ).contains(normalized)
            )
            .first()
        )

        if customer:
            return customer


    return None
