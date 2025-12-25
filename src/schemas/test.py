from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from uuid import UUID

class TestCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    user_id: UUID = Field()
    questions: list = Field(min_length=1, max_length=50)

    @field_validator('title')
    def strip_optional_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
class TestUpdate(BaseModel):
    id: UUID = Field()
    title: str = Field(min_length=1, max_length=100)
    questions: list = Field(min_length=1, max_length=100)

    @field_validator('title')
    def strip_optional_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
class TestAnswer(BaseModel):
    id: UUID = Field()
    title: str = Field(min_length=1, max_length=100)
    questions: list = Field(min_length=1, max_length=100)
    answers: list = Field(min_length=1, max_length=100)

class TestResponse(BaseModel):
    id: UUID
    title: str
    questions: list
    model_config = ConfigDict(from_attributes=True)