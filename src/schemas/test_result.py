from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from uuid import UUID

class CreateTestResult(BaseModel):
    id: UUID
    test_id: UUID
    user_id: UUID
    score: int
    max_score: int