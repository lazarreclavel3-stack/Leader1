"""Initial schema: clients, accounts, transactions, forecasts, rules, alerts, approvals, audit log.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-13 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create clients table
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("annual_revenue", sa.Float()),
        sa.Column("fiscal_year_end", sa.String(5)),
        sa.Column("qbo_realm_id", sa.String(255)),
        sa.Column("qbo_connection_date", sa.DateTime()),
        sa.Column("stripe_account_id", sa.String(255)),
        sa.Column("plaid_access_token", sa.String(255)),
        sa.Column("finch_access_token", sa.String(255)),
        sa.Column("backup_approver_email", sa.String(255)),
        sa.Column("approval_limit", sa.Float(), server_default="5000.0"),
        sa.Column("daily_safety_floor", sa.Float(), server_default="10000.0"),
        sa.Column("payroll_coverage_days", sa.Integer(), server_default="30"),
        sa.Column("settings", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default="true"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_client_email", "clients", ["email"])

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255)),
        sa.Column("role", sa.String(50)),
        sa.Column("client_id", sa.Integer()),
        sa.Column("last_login", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
    )
    op.create_index("idx_user_email", "users", ["email"])

    # Create bank_accounts table
    op.create_table(
        "bank_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("plaid_account_id", sa.String(255), unique=True),
        sa.Column("account_name", sa.String(255)),
        sa.Column("account_type", sa.String(50)),
        sa.Column("account_mask", sa.String(10)),
        sa.Column("balance", sa.Float()),
        sa.Column("balance_timestamp", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
    )
    op.create_index("idx_account_client", "bank_accounts", ["client_id"])

    # Create transactions table
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer()),
        sa.Column("plaid_transaction_id", sa.String(255), unique=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("direction", sa.String(10)),
        sa.Column("description", sa.String(255)),
        sa.Column("merchant", sa.String(255)),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("category", sa.String(100)),
        sa.Column("confidence", sa.Float()),
        sa.Column("qbo_account", sa.String(255)),
        sa.Column("qbo_journal_entry_id", sa.String(255)),
        sa.Column("flagged", sa.Boolean(), server_default="false"),
        sa.Column("flag_reason", sa.String(255)),
        sa.Column("manually_reviewed", sa.Boolean(), server_default="false"),
        sa.Column("reviewed_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["bank_accounts.id"]),
    )
    op.create_index("idx_transaction_client", "transactions", ["client_id"])
    op.create_index("idx_transaction_date", "transactions", ["date"])

    # Create cash_forecasts table
    op.create_table(
        "cash_forecasts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("week_start", sa.DateTime(), nullable=False),
        sa.Column("week_end", sa.DateTime(), nullable=False),
        sa.Column("opening_balance", sa.Float()),
        sa.Column("projected_income", sa.Float()),
        sa.Column("projected_expenses", sa.Float()),
        sa.Column("closing_balance", sa.Float()),
        sa.Column("assumptions", sa.JSON()),
        sa.Column("generated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
    )
    op.create_index("idx_forecast_client_week", "cash_forecasts", ["client_id", "week_start"])

    # Create rules table
    op.create_table(
        "rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("rule_type", sa.String(50)),
        sa.Column("threshold", sa.Float()),
        sa.Column("condition", sa.String(255)),
        sa.Column("enabled", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
    )
    op.create_index("idx_rule_client", "rules", ["client_id"])

    # Create alerts table
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("rule_id", sa.Integer()),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("severity", sa.String(20)),
        sa.Column("data", sa.JSON()),
        sa.Column("dismissed", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("dismissed_at", sa.DateTime()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["rule_id"], ["rules.id"]),
    )
    op.create_index("idx_alert_client_created", "alerts", ["client_id", "created_at"])

    # Create approvals table
    op.create_table(
        "approvals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("approver_email", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("approval_timestamp", sa.DateTime()),
        sa.Column("executed_timestamp", sa.DateTime()),
        sa.Column("reference", sa.String(255)),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
    )
    op.create_index("idx_approval_client_status", "approvals", ["client_id", "status"])

    # Create audit_log table (append-only)
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor", sa.String(255), nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("entity_type", sa.String(50)),
        sa.Column("entity_id", sa.Integer()),
        sa.Column("description", sa.Text()),
        sa.Column("details", sa.JSON()),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_audit_actor_timestamp", "audit_log", ["actor", "timestamp"])
    op.create_index("idx_audit_entity", "audit_log", ["entity_type", "entity_id"])


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("approvals")
    op.drop_table("alerts")
    op.drop_table("rules")
    op.drop_table("cash_forecasts")
    op.drop_table("transactions")
    op.drop_table("bank_accounts")
    op.drop_table("users")
    op.drop_table("clients")
