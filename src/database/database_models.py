from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric, ARRAY, String
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mydatabase"

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default='user')

    question = relationship("Question", back_populates="user")
    created_tests = relationship("Test", back_populates="user")
    test_results = relationship("TestResult", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    question : Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)
    answer_options: Mapped[list]  = mapped_column(ARRAY(String), default=[])
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    user = relationship("User", back_populates="questions")
    tests = relationship("Test", secondary='test_question', back_populates="questions")


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    answers: Mapped[list] = mapped_column(ARRAY(String), default=[])
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    creator = relationship("User", back_populates="created_tests")
    questions = relationship("Question", secondary='test_question', back_populates="tests")
    results = relationship("TestResult", back_populates="test", cascade="all, delete-orphan")


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[int] = mapped_column(default=0)
    max_score: Mapped[int] = mapped_column(default=0)

    test = relationship("Test", back_populates="results")
    user = relationship("User", back_populates="test_results")


class TestQuestionAssociation(Base):
    __tablename__='test_question'

    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"), primary_key=True)
    questions_id : Mapped[UUID] = mapped_column(ForeignKey("questions.id"), primary_key=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()