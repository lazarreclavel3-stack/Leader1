"""SQLAlchemy ORM models for Robo_CFO."""

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Boolean,
    Text,
    JSON,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Client(Base):
    """Client account with configuration and settings."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))

    # Financial info
    annual_revenue = Column(Float)
    fiscal_year_end = Column(String(5))  # MM-DD format

    # Platform connections
    qbo_realm_id = Column(String(255))
    qbo_connection_date = Column(DateTime)
    stripe_account_id = Column(String(255))
    plaid_access_token = Column(String(255))
    finch_access_token = Column(String(255))

    # Settings
    backup_approver_email = Column(String(255))
    approval_limit = Column(Float, default=5000.0)
    daily_safety_floor = Column(Float, default=10000.0)
    payroll_coverage_days = Column(Integer, default=30)

    settings = Column(JSON, default={})

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="client")
    accounts = relationship("BankAccount", back_populates="client")
    forecasts = relationship("CashForecast", back_populates="client")
    rules = relationship("Rule", back_populates="client")
    alerts = relationship("Alert", back_populates="client")
    approvals = relationship("Approval", back_populates="client")

    __table_args__ = (Index("idx_client_email", "email"),)


class BankAccount(Base):
    """Connected bank account from Plaid."""

    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    plaid_account_id = Column(String(255), unique=True)
    account_name = Column(String(255))
    account_type = Column(String(50))  # checking, savings, credit
    account_mask = Column(String(10))
    balance = Column(Float)
    balance_timestamp = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    active = Column(Boolean, default=True)

    client = relationship("Client", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

    __table_args__ = (Index("idx_account_client", "client_id"),)


class Transaction(Base):
    """Bank transaction from Plaid, categorized by agent."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("bank_accounts.id"))

    plaid_transaction_id = Column(String(255), unique=True)
    amount = Column(Float, nullable=False)
    direction = Column(String(10))  # debit, credit
    description = Column(String(255))
    merchant = Column(String(255))
    date = Column(DateTime, nullable=False)

    # AI categorization
    category = Column(String(100))
    confidence = Column(Float)  # 0-1
    qbo_account = Column(String(255))
    qbo_journal_entry_id = Column(String(255))

    # Flags for manual review
    flagged = Column(Boolean, default=False)
    flag_reason = Column(String(255))
    manually_reviewed = Column(Boolean, default=False)
    reviewed_by = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="transactions")
    account = relationship("BankAccount", back_populates="transactions")

    __table_args__ = (
        Index("idx_transaction_client", "client_id"),
        Index("idx_transaction_date", "date"),
    )


class CashForecast(Base):
    """13-week cash flow forecast."""

    __tablename__ = "cash_forecasts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    week_start = Column(DateTime, nullable=False)
    week_end = Column(DateTime, nullable=False)

    opening_balance = Column(Float)
    projected_income = Column(Float)
    projected_expenses = Column(Float)
    closing_balance = Column(Float)

    assumptions = Column(JSON)  # payroll schedule, tax dates, Stripe lag, etc.
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="forecasts")

    __table_args__ = (
        Index("idx_forecast_client_week", "client_id", "week_start"),
    )


class Rule(Base):
    """Financial rule (threshold, check, alert trigger)."""

    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    rule_type = Column(String(50))  # safety_floor, payroll_coverage, deadline, unusual_spending
    threshold = Column(Float)
    condition = Column(String(255))  # operator: <, >, ==, contains

    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="rules")
    alerts = relationship("Alert", back_populates="rule")

    __table_args__ = (Index("idx_rule_client", "client_id"),)


class Alert(Base):
    """Alert generated by a rule evaluation."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("rules.id"))

    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(String(20))  # info, warning, critical

    data = Column(JSON)  # supporting data for the alert
    dismissed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    dismissed_at = Column(DateTime)

    client = relationship("Client", back_populates="alerts")
    rule = relationship("Rule", back_populates="alerts")

    __table_args__ = (
        Index("idx_alert_client_created", "client_id", "created_at"),
    )


class Approval(Base):
    """Payment approval request with audit trail."""

    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    approver_email = Column(String(255), nullable=False)

    status = Column(String(50), default="pending")  # pending, approved, rejected, executed
    approval_timestamp = Column(DateTime)
    executed_timestamp = Column(DateTime)

    reference = Column(String(255))  # bill ID, tax payment ID, etc.

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="approvals")

    __table_args__ = (
        Index("idx_approval_client_status", "client_id", "status"),
    )


class AuditLog(Base):
    """Append-only audit log of all reads, writes, alerts, and approvals."""

    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)

    actor = Column(String(255), nullable=False)  # user email, agent name, system
    action = Column(String(50), nullable=False)  # read, write, delete, alert, approval, login

    entity_type = Column(String(50))  # Client, Transaction, Rule, etc.
    entity_id = Column(Integer)

    description = Column(Text)
    details = Column(JSON)  # what changed, IP, user agent, etc.

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        Index("idx_audit_actor_timestamp", "actor", "timestamp"),
        Index("idx_audit_entity", "entity_type", "entity_id"),
    )


class User(Base):
    """User account for login and approval."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255))

    role = Column(String(50))  # owner, backup_approver, reviewer, admin
    client_id = Column(Integer, ForeignKey("clients.id"))

    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    active = Column(Boolean, default=True)

    __table_args__ = (Index("idx_user_email", "email"),)
