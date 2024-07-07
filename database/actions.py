# import json
# import bcrypt
# from datetime import datetime
import utils
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy import event

from models import (
    Expense,
    ExpenseCategory,
    Income,
    IncomeSource,
    Account,
    Person,
    session,
)


def add_expense(date, amount, category_id, account_id, notes):
    expense = Expense(
        date=date,
        amount=amount,
        category_id=category_id,
        account_id=account_id,
        notes=notes,
    )
    session.add(expense)
    session.flush()


def add_category(name):
    category = ExpenseCategory(name=name)
    session.add(category)
    session.flush()


def add_income(date, amount, source_id, account_id, notes):
    income = Income(
        date=date,
        amount=amount,
        source_id=source_id,
        account_id=account_id,
        notes=notes,
    )
    session.add(income)
    session.flush()


def add_income_source(name):
    source = IncomeSource(name=name)
    session.add(source)
    session.flush()


def add_account(name, balance=Decimal(0)):
    account = Account(name=name, balance=balance)
    session.add(account)
    session.flush()


def add_person(name, balance=Decimal(0)):
    if session.query(Person).filter_by(name=name).first():
        utils.error(f"Person {name} already exists")
        return

    if not session.query(ExpenseCategory).filter_by(name=name).first():
        category = ExpenseCategory(name=name)
        session.add(category)
    else:
        category = session.query(ExpenseCategory).filter_by(name=name).first()

    if not session.query(IncomeSource).filter_by(name=name).first():
        source = IncomeSource(name=name)
        session.add(source)
    else:
        source = session.query(IncomeSource).filter_by(name=name).first()

    session.flush()

    if category and source:
        person = Person(
            name=name, debit_id=category.id, credit_id=source.id, balance=balance
        )
        session.add(person)
        session.flush()


def list_categories():
    categories = session.query(ExpenseCategory).all()
    for category in categories:
        print(f"ID: {category.id}, Name: {category.name}")


def list_expense(date):
    expenses = session.query(Expense).filter_by(date=date).all()
    for expense in expenses:
        print(
            f"ID: {expense.id}, Date: {expense.date}, Amount: {expense.amount:.2f}, Category ID: {expense.category_id}, account_id: {expense.account_id}, Notes: {expense.notes}"
        )


@event.listens_for(Income, "after_insert")
def after_insert_incom(mapper, connection, target):
    account = target.account
    account.balance += target.amount


@event.listens_for(Income, "after_delete")
def after_delete_income(mapper, connection, target):
    account = target.account
    account.balance -= target.amount


@event.listens_for(Expense, "after_insert")
def after_insert_expense(mapper, connection, target):
    account = target.account
    account.balance -= target.amount


@event.listens_for(Expense, "after_delete")
def after_delete_expense(mapper, connection, target):
    account = target.account
    account.balance += target.amount


if __name__ == "__main__":
    # add_expense(datetime(2021, 1, 1), Decimal(100), 1, 1, "Test expense")
    # add_category("Test category")
    # add_income(datetime(2021, 1, 1), Decimal(100), 1, 1, "Test income")
    # add_income_source("Test source")
    # add_account("Test account")
    add_person("Justin")

    session.commit()
    session.close()
