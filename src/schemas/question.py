from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from uuid import UUID

class QuestionCreate(BaseModel):
    user_id: UUID = Field()
    question: str = Field(max_length=2000)
    answer: str = Field(max_length=2000)
    answer_options: Optional[list[str]] = None

    @field_validator('question', 'answer')
    def strip_optional_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
    @field_validator('answer_options')
    def count_options(cls, v):
        if len(v) > 5 or len(v) < 2:
            raise ValueError('Количество вариантов ответа слишком велико либо слишком мало')
        return v

class QuestionUpdate(BaseModel):
    id: UUID = Field()
    user_id: UUID = Field()
    question: Optional[str] = Field(max_length=2000)
    answer: Optional[str] = Field(max_length=2000)
    answer_options: Optional[list[str]] = None


    @field_validator('question', 'answer')
    def strip_optional_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
    @field_validator('answer_options')
    def count_options(cls, v):
        if len(v) > 5 or len(v) < 2:
            raise ValueError('Количество вариантов ответа слишком велико либо слишком мало')
        return v

class QuestionResponse(BaseModel):
    id: UUID
    question: str
    answer: str
    answer_options: Optional[list[str]]
    model_config = ConfigDict(from_attributes=True)