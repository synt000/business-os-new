import os
import sys

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.database import Base
import src.models.saas_core
import src.feedback.models

# AUTO LOAD ALL DOMAIN MODELS
import pkgutil
import importlib
import src.domains

for _, module_name, _ in pkgutil.walk_packages(
    src.domains.__path__,
    src.domains.__name__ + "."
):
    if module_name.endswith(".models"):
        importlib.import_module(module_name)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


LEGACY_IGNORE_TABLES = {
    "social_webhooks",
    "login_sessions",
    "refresh_tokens",
    "tenant_partnerships",
    "franchise_networks",
    "predictive_analytics",
    "subscriptions",
}




LEGACY_IGNORE_COLUMNS = {
    "activation_keys": {
        "key",
    },

    "business_profiles": {
        "theme_color",
        "email",
        "owner_phone",
        "cover_url",
        "owner_name",
        "business_slug",
        "viber_number",
        "website_url",
        "qr_code",
        "welcome_message",
        "facebook_url",
        "facebook_username",
        "is_public",
        "telegram_url",
        "business_type_code",
        "telegram_username",
    },

    "subscription_payments": {
        "transaction_ref",
        "plan_id",
        "method",
    },
}


def include_object(object, name, type_, reflected, compare_to):

    # Ignore legacy tables
    if type_ == "table" and reflected and name in LEGACY_IGNORE_TABLES:
        return False

    # Ignore legacy columns
    if type_ == "column" and reflected:
        table_name = object.table.name

        if table_name in LEGACY_IGNORE_COLUMNS:
            if name in LEGACY_IGNORE_COLUMNS[table_name]:
                return False

    # Ignore activation_keys index/fk drift
    if type_ in {"index", "foreign_key_constraint"}:
        if getattr(object, "table", None) is not None:
            if object.table.name == "activation_keys":
                if name in {
                    "ix_activation_keys_key",
                    "ix_activation_keys_key_code",
                    None,
                }:
                    return False

    return True




def run_migrations_offline():
    url = os.getenv("DATABASE_URL")

    if not url:
        url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = os.getenv("DATABASE_URL")

    if not url:
        url = config.get_main_option("sqlalchemy.url")

    connectable = engine_from_config(
        {
            "sqlalchemy.url": url
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
