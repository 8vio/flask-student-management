from typing import Dict, List, Union
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class CoursesCreationSchema(PydanticBaseModel):
    course_name: str

    class Config:
        allow_population_by_field_name = True


class CourseSchema(PydanticBaseModel):
    
    id_course: int
    course_name:  str
    dt_created: datetime
    ic_active:  bool

    class Config:
        orm_mode = True


class CoursesSchema(PydanticBaseModel):
    courses: List[Union[CourseSchema, Dict]] = Field(...)

    class Config:
        allow_population_by_field_name = True