import datetime
from enum import Enum as PyEnum
from decimal import Decimal

from sqlalchemy import Numeric, Enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    DeclarativeBase,
)


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("expense_categories.id"), nullable=False
    )
    notes: Mapped[str]
    category: Mapped["ExpenseCategory"] = relationship(back_populates="expenses")
    account: Mapped["Account"] = relationship(back_populates="expenses")

    def get_attributes(self):
        return ["id", "date", "amount", "account_id", "category_id", "notes"]

    def get_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "account": self.account.name,
            "category": self.category.name,
            "notes": self.notes,
        }

    def __repr__(self) -> str:
        return (
            f"<Expense(id={self.id}, date={self.date}, amount={self.amount:.2f}, "
            f"account_id={self.account_id}, category_id={self.category_id}, notes={self.notes})>"
        )


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

    def get_attributes(self):
        return ["id", "name"]

    def get_dict(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self) -> str:
        return f"<ExpenseCategory(id={self.id}, name='{self.name}')>"


class Income(Base):
    __tablename__ = "incomes"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    source_id: Mapped[int] = mapped_column(
        ForeignKey("income_sources.id"), nullable=False
    )
    notes: Mapped[str]
    source: Mapped["IncomeSource"] = relationship(back_populates="incomes")
    account: Mapped["Account"] = relationship(back_populates="incomes")

    def get_attributes(self):
        return ["id", "date", "amount", "account_id", "source_id", "notes"]

    def get_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "account": self.account.name,
            "source": self.source.name,
            "notes": self.notes,
        }

    def __repr__(self) -> str:
        return (
            f"<Income(id={self.id}, date={self.date}, amount={self.amount:.2f}, "
            f"account_id={self.account_id}, source_id={self.source_id}, notes={self.notes})>"
        )


class IncomeSource(Base):
    __tablename__ = "income_sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    incomes: Mapped[list["Income"]] = relationship(back_populates="source")

    def get_attributes(self):
        return ["id", "name"]

    def get_dict(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self) -> str:
        return f"<IncomeSource(id={self.id}, name='{self.name}')>"


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="account")
    incomes: Mapped[list["Income"]] = relationship(back_populates="account")

    def get_attributes(self):
        return ["id", "name", "balance"]

    def get_dict(self):
        return {"id": self.id, "name": self.name, "balance": self.balance}

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, name='{self.name}', balance={self.balance})>"


class Person(Base):
    __tablename__ = "persons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transactions: Mapped[list["PersonTransaction"]] = relationship(
        back_populates="person"
    )

    def get_attributes(self):
        return ["id", "name", "balance"]

    def get_dict(self):
        return {"id": self.id, "name": self.name, "balance": self.balance}

    def __repr__(self) -> str:
        return f"<Person(id={self.id}, name='{self.name}', balance={self.balance})>"


class TransactionType(str, PyEnum):
    DEBIT = "debit"
    CREDIT = "credit"


class PersonTransaction(Base):
    __tablename__ = "person_transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), nullable=False
    )
    notes: Mapped[str]
    person: Mapped["Person"] = relationship(back_populates="transactions")

    def get_attributes(self):
        return [
            "id",
            "date",
            "amount",
            "person_id",
            "transaction_type",
            "notes",
        ]

    def get_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "person": self.person.name,
            "transaction_type": self.transaction_type,
            "notes": self.notes,
        }

    def __repr__(self) -> str:
        return (
            f"<PersonTransaction(id={self.id}, date={self.date}, amount={self.amount:.2f}, "
            f"person_id={self.person_id}, transaction_type={self.transaction_type}, notes={self.notes})>"
        )


# Base.metadata.create_all(engine)
