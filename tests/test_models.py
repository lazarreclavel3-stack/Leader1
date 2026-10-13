"""Tests for Robo_CFO models and audit logging."""

import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from robo_cfo.models import Base, Client, User, AuditLog
from robo_cfo.audit import log_write, log_read, log_login


@pytest.fixture
async def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield session_maker

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_client(test_db):
    """Test creating a client and logging the write."""
    async with test_db() as session:
        # Create client
        client = Client(
            name="Therapy Practice",
            email="owner@therapypractice.com",
            annual_revenue=2000000.0,
            fiscal_year_end="12-31",
            active=True,
        )
        session.add(client)
        await session.flush()

        # Log the creation
        await log_write(
            session,
            actor="clavel@lazarre.com",
            entity_type="Client",
            entity_id=client.id,
            description="Created new client: Therapy Practice",
            changes={"name": "Therapy Practice", "email": "owner@therapypractice.com"},
        )
        await session.commit()

        # Verify client exists
        assert client.id is not None
        assert client.name == "Therapy Practice"
        assert client.active is True

        # Verify audit log entry
        result = await session.execute("SELECT * FROM audit_log WHERE entity_type = 'Client'")
        audit_entries = result.fetchall()
        assert len(audit_entries) > 0


@pytest.mark.asyncio
async def test_create_user(test_db):
    """Test creating a user."""
    async with test_db() as session:
        client = Client(
            name="Test Practice",
            email="test@example.com",
            active=True,
        )
        session.add(client)
        await session.flush()

        user = User(
            email="owner@example.com",
            role="owner",
            client_id=client.id,
            active=True,
        )
        session.add(user)

        await session.commit()

        assert user.id is not None
        assert user.email == "owner@example.com"
        assert user.role == "owner"


@pytest.mark.asyncio
async def test_audit_logging(test_db):
    """Test audit log entries are created for all operations."""
    async with test_db() as session:
        # Simulate a series of operations
        await log_login(session, "owner@example.com", "192.168.1.1")

        # Create a client
        client = Client(
            name="Test Client",
            email="client@example.com",
            active=True,
        )
        session.add(client)
        await session.flush()

        await log_write(
            session,
            actor="clavel@lazarre.com",
            entity_type="Client",
            entity_id=client.id,
            description="Created new client",
        )

        # Read operation
        await log_read(
            session,
            actor="owner@example.com",
            entity_type="Client",
            entity_id=client.id,
            description="Viewed client details",
        )

        await session.commit()

        # Verify audit log has entries
        result = await session.execute("SELECT COUNT(*) FROM audit_log")
        count = result.scalar()
        assert count >= 3  # login, write, read
