from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)
    role: str = Field(default='user')
    
    @field_validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v
    
    @field_validator('role')
    def role_type(cls, v, values):
        if v not in ['user', 'admin']:
            raise ValueError('Не корректный тип пользователя')
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    
    class Config:
        orm_mode = True