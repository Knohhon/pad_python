from sqlalchemy.orm import Session
from src.database.database_models import Test, User, TestResult, Question
from src.schemas.test import TestCreate, TestUpdate, TestAnswer
from src.schemas.test_result import CreateTestResult
from uuid import UUID

def get_test(db: Session, test_id: UUID) -> Test:
    return db.query(Test).filter(Test.id == test_id)

def get_tests(db: Session, test_id_list: list[UUID]) -> list[Test]:
    return db.query(Test).filter(Test.id in test_id_list).all()

def get_all_tests(db: Session) -> list[Test]:
    return db.query(Test).all()


def answer_test(db: Session, test: TestAnswer, current_user: User) -> TestResult:
    if len(test.questions) != len(test.answers):
        raise "ValueError"
    
    result = CreateTestResult(
        user_id=current_user.id,
        test_id=test.id,
        score=0,
        max_score=len(test.questions)
    )

    for idx in range(len(test.questions)):
        db_current_question = Question(
            id = test.questions[idx]
        )
        result = db.execute(db_current_question)
        question_from_db = result.scalar_one_or_none()

        if question_from_db.answer == test.answers[idx]:
            score += 1
        
    return result
            
 
def update_test(db: Session, test: TestUpdate, current_user: User) -> Test:
    db_test = Test(
        id=test.id,
        user_id=current_user.id,
        questions=test.questions
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def create_test(db: Session, test: TestCreate, current_user: User):
    db_test = Test(
        title=test.title,
        user_id=current_user.id,
        questions=test.questions
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test