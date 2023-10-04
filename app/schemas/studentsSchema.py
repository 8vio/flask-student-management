from typing import Dict, List, Union
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr, Field


class StudentCreationSchema(PydanticBaseModel):
    first_name: str
    family_name: str
    date_birth: str
    email_address: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True



class StudentSchema(PydanticBaseModel):
    
    id_student: int
    first_name:  str
    family_name: str
    date_birth:  datetime
    email_address:  EmailStr
    dt_created: datetime
    ic_active:  bool

    class Config:
        orm_mode = True


class StudentsSchema(PydanticBaseModel):
    students: List[Union[StudentSchema, Dict]] = Field(...)

    class Config:
        allow_population_by_field_name = True