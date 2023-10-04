from pydantic import BaseModel as PydanticBaseModel


class LoginSchema(PydanticBaseModel):
    username: str
    password: str
    
    class Config:
        allow_population_by_field_name = True
