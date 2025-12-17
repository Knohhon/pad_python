from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from database.models import Test, Question, User
from crud import question_crud
from database.database import get_db
from utils.check_role import get_current_admin
from utils.security import get_current_user

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/create")
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin)
    ):
    
    new_question = question_crud.create_question(db, question, user)
    return new_question

@router.post("/update")
def update_question(
    question: QuestionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin)
):
    
    updated_question = question_crud.update_question(db, question, user)
    return updated_question

@router.get("/")
def get_all_questions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    questions = question_crud.get_all_questions(db)
    return questions