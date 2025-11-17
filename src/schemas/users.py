from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

class UserGetSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
