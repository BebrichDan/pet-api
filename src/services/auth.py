from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    create_access_token,
    create_refresh_token_raw,
    hash_refresh_token,
)
from src.core.settings import settings
from src.models.refresh_tokens import RefreshTokenModel


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tokens_for_user(self, user):
        raw_refresh = create_refresh_token_raw()
        token_hash = hash_refresh_token(raw_refresh)
        issued = datetime.utcnow()
        expires = issued + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        refresh_model = RefreshTokenModel(
            user_id=user.id,
            token_hash=token_hash,
            issued_at=issued,
            expires_at=expires,
            revoked=False,
        )
        self.session.add(refresh_model)
        await self.session.commit()
        await self.session.refresh(refresh_model)

        access = create_access_token(subject=str(user.id))
        return {
            "access_token": access,
            "refresh_token": raw_refresh,
            "refresh_expires_at": expires,
        }

    async def revoke_refresh(self, raw_refresh_token: str):
        hash_ = hash_refresh_token(raw_refresh_token)
        q = (
            select(RefreshTokenModel)
            .where(RefreshTokenModel.token_hash == hash_)
        )
        res = await self.session.execute(q)
        model = res.scalar_one_or_none()
        if not model:
            return False
        model.revoked = True
        await self.session.commit()
        return True

    async def rotate_refresh(self, raw_refresh_token: str):
        hash_ = hash_refresh_token(raw_refresh_token)
        q = (
            select(RefreshTokenModel)
            .where(RefreshTokenModel.token_hash == hash_)
        )
        res = await self.session.execute(q)
        model = res.scalar_one_or_none()

        if not model or model.revoked:
            return None

        if model.expires_at <= datetime.utcnow():
            return None

        model.revoked = True
        await self.session.commit()

        user = model.user
        auth = AuthService(self.session)
        return await auth.create_tokens_for_user(user)
