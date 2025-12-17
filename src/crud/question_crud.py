from sqlalchemy.orm import Session
from database.models import Question, User
from schemas.question import QuestionCreate, QuestionUpdate
from uuid import UUID

def get_question(db: Session, question_id: UUID) -> Question:
    return db.query(Question).filter(Question.id == question_id)

def get_questions(db: Session, question_id_list: list[UUID]) -> list[Question]:
    return db.query(Question).filter(Question.id in question_id_list).all()

def get_all_questions(db: Session) -> list[Question]:
    return db.query(Question).all()

def update_question(db: Session, question: QuestionUpdate, current_user: User) -> Question:
    db_question = Question(
        question_id=question.id,
        user_id=current_user.id,
        question=question.question,
        answer=question.answer,
        answer_options=question.answer_options
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def create_question(db: Session, question: QuestionCreate, current_user: User):
    db_question = Question(
        user_id=current_user.id,
        question=question.question,
        answer=question.answer,
        answer_options=question.answer_options
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question