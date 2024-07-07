import datetime
from decimal import Decimal

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Numeric

from sqlalchemy import create_engine, String, ForeignKey, select, func
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    Mapped,
    mapped_column,
    DeclarativeBase,
)

DATABASE_URL = "sqlite+pysqlite:///database/expense_tracker.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("expense_categories.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    notes: Mapped[str]
    category: Mapped["ExpenseCategory"] = relationship(back_populates="expenses")
    account: Mapped["Account"] = relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return (
            f"<Expense(id={self.id}, date={self.date}, amount={self.amount:.2f}, "
            f"category_id={self.category_id}, account_id={self.account_id}, notes={self.notes})>"
        )


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<ExpenseCategory(id={self.id}, name='{self.name}')>"


class Income(Base):
    __tablename__ = "incomes"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    source_id: Mapped[int] = mapped_column(
        ForeignKey("income_sources.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    notes: Mapped[str]
    source: Mapped["IncomeSource"] = relationship(back_populates="incomes")
    account: Mapped["Account"] = relationship(back_populates="incomes")

    def __repr__(self) -> str:
        return (
            f"<Income(id={self.id}, date={self.date}, amount={self.amount:.2f}, "
            f"source_id={self.source_id}, account_id={self.account_id}, notes={self.notes})>"
        )


class IncomeSource(Base):
    __tablename__ = "income_sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    incomes: Mapped[list["Income"]] = relationship(back_populates="source")

    def __repr__(self) -> str:
        return f"<IncomeSource(id={self.id}, name='{self.name}')>"


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="account")
    incomes: Mapped[list["Income"]] = relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, name='{self.name}', balance={self.balance})>"


class Person(Base):
    __tablename__ = "persons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    debit_id: Mapped[int] = mapped_column(
        ForeignKey("expense_categories.id"), nullable=False
    )
    credit_id: Mapped[int] = mapped_column(
        ForeignKey("income_sources.id"), nullable=False
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    debit: Mapped["ExpenseCategory"] = relationship()
    credit: Mapped["IncomeSource"] = relationship()

    def __repr__(self) -> str:
        return (
            f"<Person(id={self.id}, name='{self.name}', "
            f"debit_id={self.debit_id}, credit_id={self.credit_id}, balance={self.balance})>"
        )


# Base.metadata.create_all(engine)
