from sqlalchemy.orm import Session
from sqlalchemy import func

from src.domains.accounting.models import AccountLedger


def get_finance_summary(
    db: Session,
    tenant_id: str
):
    """
    Enterprise Ledger Based Finance Engine V2
    Source of Truth:
    AccountLedger
    """

    # =========================
    # REVENUE
    # =========================

    revenue = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.entry_type == "CREDIT",
            AccountLedger.account_head.in_(["SALES_REVENUE","RENTAL_PAYMENT","SUBSCRIPTION_REVENUE"])
        )
        .scalar()
    )


    # =========================
    # COGS
    # =========================

    cogs = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.entry_type == "DEBIT",
            AccountLedger.account_head == "COGS_EXPENSE"
        )
        .scalar()
    )


    # =========================
    # CASH FLOW
    # =========================

    cash_in = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.entry_type == "DEBIT",
            AccountLedger.account_head == "CASH_ASSET"
        )
        .scalar()
    )


    cash_out = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.entry_type == "CREDIT",
            AccountLedger.account_head == "CASH_ASSET"
        )
        .scalar()
    )


    gross_profit = (
        revenue or 0
    ) - (
        cogs or 0
    )


    profit_margin = 0

    if revenue:
        profit_margin = round(
            (gross_profit / revenue) * 100,
            2
        )


    return {
        "revenue": float(revenue or 0),
        "cogs": float(cogs or 0),
        "gross_profit": float(gross_profit),
        "cash_in": float(cash_in or 0),
        "cash_out": float(cash_out or 0),
        "net_cash_flow": float(
            (cash_in or 0) - (cash_out or 0)
        ),
        "profit_margin": profit_margin
    }


def get_finance_health_score(
    db: Session,
    tenant_id: str
):

    finance = get_finance_summary(
        db,
        tenant_id
    )

    score = 0


    if finance["gross_profit"] > 0:
        score += 30


    if finance["net_cash_flow"] > 0:
        score += 30


    if finance["revenue"] > 0:
        score += 25


    if finance["profit_margin"] >= 20:
        score += 15


    status = "WARNING"

    if score >= 80:
        status = "EXCELLENT"

    elif score >= 50:
        status = "NORMAL"


    return {
        "score": score,
        "status": status,
        "details": finance
    }

