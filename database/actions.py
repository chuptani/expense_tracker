import utils
from utils.logger import cli_logger
from decimal import Decimal
from sqlalchemy import event

from database.models import (
    Expense,
    ExpenseCategory,
    Income,
    IncomeSource,
    Account,
    Person,
    session,
)


def add_expense(date, amount, account_id, category_id, notes):
    expense = Expense(
        date=date,
        amount=amount,
        account_id=account_id,
        category_id=category_id,
        notes=notes,
    )
    session.add(expense)
    session.flush()
    expense.account.balance -= amount
    session.flush()
    # cli_logger.info(f"Expense '{expense.notes}' added successfully")


def delete_expense(expense_id):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        expense.account.balance -= expense.amount
        session.delete(expense)
        session.flush()
    else:
        cli_logger.error(f"Expense with ID {expense_id} does not exist")


def add_category(name):
    if session.query(ExpenseCategory).filter_by(name=name).first():
        cli_logger.error(f"Category {name} already exists")
        return
    category = ExpenseCategory(name=name)
    session.add(category)
    session.flush()


def delete_category(category_id):
    category = session.query(ExpenseCategory).filter_by(id=category_id).first()
    if category:
        session.delete(category)
        session.flush()
    else:
        cli_logger.error(f"Category with ID {category_id} does not exist")


def get_categories():
    return session.query(ExpenseCategory).all()


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
    income.account.balance += amount
    session.flush()


def delete_income(income_id):
    income = session.query(Income).filter_by(id=income_id).first()
    if income:
        session.delete(income)
        session.flush()
    else:
        cli_logger.error(f"Income with ID {income_id} does not exist")


def add_income_source(name):
    if session.query(IncomeSource).filter_by(name=name).first():
        cli_logger.error(f"Income source {name} already exists")
        return
    source = IncomeSource(name=name)
    session.add(source)
    session.flush()


def delete_income_source(source_id):
    source = session.query(IncomeSource).filter_by(id=source_id).first()
    if source:
        session.delete(source)
        session.flush()
    else:
        cli_logger.error(f"Income source with ID {source_id} does not exist")


def add_account(name, balance=Decimal(0)):
    if session.query(Account).filter_by(name=name).first():
        cli_logger.error(f"Account {name} already exists")
        return
    account = Account(name=name, balance=balance)
    session.add(account)
    session.flush()


def delete_account(account_id):
    account = session.query(Account).filter_by(id=account_id).first()
    if account:
        session.delete(account)
        session.flush()
    else:
        cli_logger.error(f"Account with ID {account_id} does not exist")


def get_accounts():
    return session.query(Account).all()


def add_person(name, balance=Decimal(0)):
    if session.query(Person).filter_by(name=name).first():
        cli_logger.error(f"Person {name} already exists")
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


def delete_person(person_id):
    person = session.query(Person).filter_by(id=person_id).first()
    if person:
        session.delete(person)
        session.flush()
    else:
        cli_logger.error(f"Person with ID {person_id} does not exist")


# @event.listens_for(Income, "after_insert")
# def after_insert_incom(mapper, connection, target):
#     account = target.account
#     account.balance += target.amount
#
#
# @event.listens_for(Income, "after_delete")
# def after_delete_income(mapper, connection, target):
#     account = target.account
#     account.balance -= target.amount
#
#
# @event.listens_for(Expense, "after_insert")
# def after_insert_expense(mapper, connection, target):
#     account = target.account
#     account.balance -= target.amount
#
#
# @event.listens_for(Expense, "after_delete")
# def after_delete_expense(mapper, connection, target):
#     account = target.account
#     account.balance += target.amount
