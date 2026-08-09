import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.saas_core import (
    Invoice,
    Tenant,
    Customer,
    Order,
    Payment,
    Receivable,
    OrderItem,
    CustomerIdentity,
)
from src.domains.product.models import Product
from src.domains.inventory.models import Inventory
from src.domains.movement.models import StockMovement
from src.domains.audit.models import AuditLog
from src.domains.accounting.models import AccountLedger
from src.domains.payment.webhook.event import WebhookEvent
from src.domains.subscription.models import (
    SubscriptionPlan,
    TenantSubscription,
    SubscriptionPayment,
)
from src.core.database import Base
from src.domains.social_center.models import SocialChannel
from src.domains.social_post.models import SocialPost
from src.domains.social_post.publish_log_models import SocialPublishLog
from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.campaign.execution_models import CampaignExecutionLog


import os

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///./test_business.db",
)

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

Base.metadata.create_all(
    bind=engine,
    tables=[
        Tenant.__table__,
        Customer.__table__,
        Order.__table__,
        Invoice.__table__,
        Payment.__table__,
        Receivable.__table__,
        OrderItem.__table__,
        Product.__table__,
        Inventory.__table__,
        StockMovement.__table__,
        AuditLog.__table__,
        AccountLedger.__table__,
        CustomerIdentity.__table__,
        WebhookEvent.__table__,
        SubscriptionPlan.__table__,
        TenantSubscription.__table__,
        SubscriptionPayment.__table__,
        SocialChannel.__table__,
        SocialPost.__table__,
        SocialPublishLog.__table__,
        Campaign.__table__,
        CampaignChannel.__table__,
        CampaignExecutionLog.__table__,
    ],
)

TestingSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():

    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSession(
        bind=connection
    )

    try:
        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def tenant_id(db_session):

    tenant = (
        db_session.query(Tenant)
        .filter(
            Tenant.id == "test-tenant"
        )
        .first()
    )

    if tenant:
        return tenant.id

    tenant = Tenant(
        id="test-tenant",
        company_name="Test Company",
        owner_email="test@example.com",
    )

    db_session.add(tenant)
    db_session.commit()

    return tenant.id


@pytest.fixture
def payment_data():

    class PaymentData:
        payment_request_id = None
        payment_number = "TEST-PAY"
        invoice_id = "invoice-test"
        amount = 100

    return PaymentData()


@pytest.fixture
def invoice_id(db_session, tenant_id):

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == "invoice-test"
        )
        .first()
    )

    if invoice:
        return invoice.id


    customer = Customer(
        id="customer-test",
        customer_name="Test Customer",
        tenant_id=tenant_id,
    )

    db_session.add(customer)
    db_session.flush()


    order = Order(
        id="order-test",
        order_number="ORDER-TEST-001",
        platform_channel="TEST",
        customer_name="Test Customer",
        customer_id=customer.id,
        total_amount=1000,
        order_status="CONFIRMED",
        tenant_id=tenant_id,
    )

    db_session.add(order)
    db_session.flush()


    invoice = Invoice(
        id="invoice-test",
        invoice_number="INV-TEST-001",
        tenant_id=tenant_id,
        amount=1000,
        status="UNPAID",
        order_id=order.id,
    )

    db_session.add(invoice)
    db_session.commit()

    return invoice.id
