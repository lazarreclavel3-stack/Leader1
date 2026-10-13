"""Audit logging for all reads, writes, alerts, and approvals."""

from datetime import datetime
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from robo_cfo.models import AuditLog


async def log_action(
    session: AsyncSession,
    actor: str,
    action: str,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    description: Optional[str] = None,
    details: Optional[dict[str, Any]] = None,
) -> AuditLog:
    """
    Log an action to the audit log.

    Args:
        session: Database session
        actor: User email, agent name, or 'system'
        action: read, write, delete, alert, approval, login
        entity_type: Client, Transaction, Rule, etc.
        entity_id: ID of the affected entity
        description: Human-readable description
        details: Additional context (what changed, IP, etc.)
    """
    log_entry = AuditLog(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        details=details or {},
        timestamp=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.flush()
    return log_entry


async def log_read(
    session: AsyncSession,
    actor: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    description: Optional[str] = None,
) -> AuditLog:
    """Log a read operation."""
    return await log_action(
        session,
        actor=actor,
        action="read",
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )


async def log_write(
    session: AsyncSession,
    actor: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    description: Optional[str] = None,
    changes: Optional[dict[str, Any]] = None,
) -> AuditLog:
    """Log a write operation."""
    return await log_action(
        session,
        actor=actor,
        action="write",
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        details={"changes": changes or {}},
    )


async def log_alert(
    session: AsyncSession,
    actor: str,
    client_id: int,
    alert_id: int,
    title: str,
    severity: str,
) -> AuditLog:
    """Log an alert generation."""
    return await log_action(
        session,
        actor=actor,
        action="alert",
        entity_type="Alert",
        entity_id=alert_id,
        description=f"[{severity}] {title}",
        details={"client_id": client_id, "severity": severity},
    )


async def log_approval(
    session: AsyncSession,
    actor: str,
    approval_id: int,
    status: str,
    amount: float,
    description: str,
) -> AuditLog:
    """Log an approval action."""
    return await log_action(
        session,
        actor=actor,
        action="approval",
        entity_type="Approval",
        entity_id=approval_id,
        description=f"{status}: {description} (${amount:.2f})",
        details={"status": status, "amount": amount},
    )


async def log_login(
    session: AsyncSession,
    user_email: str,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """Log a user login."""
    return await log_action(
        session,
        actor=user_email,
        action="login",
        description=f"User login from {ip_address or 'unknown'}",
        details={"ip_address": ip_address},
    )
