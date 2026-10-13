"""FastAPI application for Robo_CFO."""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from robo_cfo.database import get_session, init_db, close_db
from robo_cfo.auth import LoginRequest, LoginResponse, authenticate_user, create_access_token
from robo_cfo.models import User

app = FastAPI(title="Robo_CFO", description="Bespoke AI finance agent")


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown."""
    await close_db()


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "robo-cfo"}


@app.post("/auth/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    User login endpoint.

    Returns an access token on successful authentication.
    """
    user = await authenticate_user(session, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)
    return LoginResponse(
        access_token=access_token,
        user_id=user.id,
        email=user.email,
    )


@app.get("/auth/me")
async def me(
    session: AsyncSession = Depends(get_session),
    # Authorization header would be parsed here in production
):
    """Get current user info (placeholder)."""
    return {"detail": "Implement bearer token extraction"}


@app.get("/clients")
async def list_clients(session: AsyncSession = Depends(get_session)):
    """List all clients (view-only, placeholder)."""
    return {"clients": [], "note": "Implement per-user authorization"}


@app.get("/clients/{client_id}/dashboard")
async def get_dashboard(
    client_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Get the CFO dashboard for a client.

    Includes: cash position, 13-week forecast, alerts, next actions.
    """
    return {
        "client_id": client_id,
        "cash_position": None,
        "forecast": None,
        "alerts": [],
        "actions": [],
        "note": "Implement dashboard data queries",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "robo_cfo.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
