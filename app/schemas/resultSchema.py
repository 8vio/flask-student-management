from typing import Dict, List, Union
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class ResultsCreationSchema(PydanticBaseModel):

    cd_student: int
    cd_course: int
    score: str

    class Config:
        allow_population_by_field_name = True


class ResultSchema(PydanticBaseModel):
    
    id_result: int
    cd_student: int
    cd_course: int
    score: str
    dt_created: datetime
    ic_active:  bool

    class Config:
        orm_mode = True


class ResultsSchema(PydanticBaseModel):
    results: List[Union[ResultSchema, Dict]] = Field(...)

    class Config:
        allow_population_by_field_name = True