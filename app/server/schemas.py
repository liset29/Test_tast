from typing import Optional, Annotated, List
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from pydantic import BaseModel, EmailStr, Field, ConfigDict

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    user_name: str = Field(...)
    hashed_password: str = Field(...)
    model_config = ConfigDict(populate_by_name=True,
                              arbitrary_types_allowed=True,
                              json_schema_extra={
                                  "example": {
                                      "user_name": "abibus",
                                      "hashed_password": "bumbampup"

                                  }
                              }
                              )
class UserCollections(BaseModel):
    users: List[UserModel]