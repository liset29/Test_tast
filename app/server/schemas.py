from typing import Optional, Annotated, List, Literal
from pydantic.functional_validators import BeforeValidator
from pydantic import BaseModel, EmailStr, Field, ConfigDict

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    username: str | None = Field(...)
    email: EmailStr | None = None

class Registered(UserModel):
    id : int
    active : bool
    role: Literal['admin', 'user'] = Field()



class Registration(UserModel):
    password: str


class UserUpdate(UserModel):
    username: Optional[str] = Field(None)
    active: Optional[bool] = None
    role: Literal['admin', 'user'] = Field()


class CreateUser(UserModel):
    password: str
    role: Literal['admin', 'user'] = Field()


class UserCollections(BaseModel):
    id: int
    users: List[UserModel]





class UserSchema(UserModel):
    model_config = ConfigDict(strict=True)
    password: str
    active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
