from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)

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
    hashed_password = Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    is_active = Mapped[bool] = mapped_column(default=True)
    role = Mapped[str] = mapped_column(default='user')

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
    answer_options: Mapped[list]  = mapped_column(default=[])
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
    __tablename__='test_questions'

    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"), primary_key=True),
    questions_id : Mapped[UUID] = mapped_column(ForeignKey("questions.id"), primary_key=True),
