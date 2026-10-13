"""Authentication and authorization."""

from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from robo_cfo.models import User
from robo_cfo.database import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    """Login request payload."""

    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response with token."""

    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> Optional[User]:
    """Authenticate a user by email and password."""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not user.active:
        return None

    if not verify_password(password, user.hashed_password or ""):
        return None

    user.last_login = datetime.utcnow()
    await session.commit()
    return user


async def get_or_create_user(
    session: AsyncSession,
    email: str,
    role: str = "owner",
    client_id: Optional[int] = None,
) -> User:
    """Get or create a user."""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(
        email=email,
        role=role,
        client_id=client_id,
        created_at=datetime.utcnow(),
        active=True,
    )
    session.add(user)
    await session.commit()
    return user


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Note: This is a placeholder. Production should use python-jose for proper JWT handling.
    """
    import json
    import base64
    from datetime import datetime, timedelta

    if expires_delta is None:
        expires_delta = timedelta(hours=24)

    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),
        "exp": expire.timestamp(),
    }

    # Simple base64 encoding for now; replace with proper JWT in production
    token = base64.b64encode(json.dumps(payload).encode()).decode()
    return token


async def verify_access_token(session: AsyncSession, token: str) -> Optional[User]:
    """
    Verify and decode an access token.

    Note: This is a placeholder. Production should use python-jose for proper JWT handling.
    """
    import json
    import base64
    from datetime import datetime

    try:
        payload = json.loads(base64.b64decode(token))
        user_id = int(payload.get("sub"))
        exp = payload.get("exp")

        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return user if user and user.active else None
    except (ValueError, KeyError, TypeError):
        return None
