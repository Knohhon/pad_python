from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.schemas.test import TestCreate, TestResponse, TestUpdate
from src.database.database_models import Test, Question, User, get_db
from src.crud import test_crud
from src.utils.check_role import get_current_admin
from src.utils.security import get_current_user

router = APIRouter(prefix="/tests", tags=["questions"])

@router.post("/create")
def create_test(
    test: TestCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin)
    ):
    
    new_test = test_crud.create_question(db, test, user)
    return new_test

@router.post("/update")
def update_test(
    test: TestUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin)
):
    
    updated_test = test_crud.update_test(db, test, user)
    return updated_test

@router.post("/answer_test")
def answer_test(
    test: TestResponse,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    result = test_crud.answer_test(db, test, user)
    return result


@router.get("/")
def get_all_tests(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    tests = test_crud.get_all_tests(db)
    return tests