from typing import Dict, List, Union
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr, Field


class UserCreationSchema(PydanticBaseModel):
    st_lastname: str
    st_firstname: str
    username: str
    em_user_email: EmailStr = Field(...)
    password: str
    
    class Config:
        allow_population_by_field_name = True

class UserSchema(PydanticBaseModel):
    
    id_user: int
    st_lastname:  str
    st_firstname: str
    username: str
    em_user_email:  EmailStr
    dt_created: datetime
    ic_active:  bool

    class Config:
        orm_mode = True


class UsersSchema(PydanticBaseModel):
    users: List[Union[UserSchema, Dict]] = Field(...)

    class Config:
        allow_population_by_field_name = True