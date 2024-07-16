from typing import Optional, Annotated, List
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from pydantic import BaseModel, EmailStr, Field, ConfigDict

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    username: str = Field(...)
    password: str
    email: EmailStr | None = None
    model_config = ConfigDict(populate_by_name=True,
                              arbitrary_types_allowed=True,

                              )


class UserCollections(BaseModel):
    users: List[UserModel]


class UserSchema(UserModel):
    model_config = ConfigDict(strict=True)

    active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
