from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password, verify_password
from src.models.users import UserModel


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> UserModel | None:
        q = select(UserModel).where(UserModel.email == email)
        res = await self.session.execute(q)
        return res.scalar_one_or_none()

    async def create_user(self, email: str, password: str) -> UserModel:
        hashed = hash_password(password)
        user = UserModel(email=email, hashed_password=hashed)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def authenticate(
            self,
            email: str,
            password: str,
    ) -> UserModel | None:
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
