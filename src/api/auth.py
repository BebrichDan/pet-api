from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_session
from src.schemas.auth import TokenSchema
from src.schemas.users import UserCreateSchema, UserGetSchema
from src.services.auth import AuthService
from src.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserGetSchema)
async def signup(data: UserCreateSchema, session = Depends(get_session)):
    us = UserService(session)
    existing = await us.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await us.create_user(data.email, data.password)
    return user

@router.post("/login", response_model=TokenSchema)
async def login(data: UserCreateSchema, session = Depends(get_session)):
    us = UserService(session)
    user = await us.authenticate(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    auth = AuthService(session)
    tokens = await auth.create_tokens_for_user(user)
    return {"access_token": tokens["access_token"], "token_type": "bearer"}

@router.post("/refresh", response_model=TokenSchema)
async def refresh(refresh_request: dict, session = Depends(get_session)):
    raw_refresh = refresh_request.get("refresh_token")
    if not raw_refresh:
        raise HTTPException(400, "refresh_token required")
    auth = AuthService(session)
    new_pair = await auth.rotate_refresh(raw_refresh)
    if not new_pair:
        raise HTTPException(401, "Invalid or expired refresh token")
    return {"access_token": new_pair["access_token"], "token_type": "bearer"}
