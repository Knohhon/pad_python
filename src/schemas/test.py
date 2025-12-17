from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from uuid import UUID

class TestCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    user_id: UUID = Field()

class TestUpdate(BaseModel):
    pass

class TestResponse(BaseModel):
    pass