import logging
from utils.logger import BasicFormatter
from decimal import Decimal

# from sqlalchemy import event

from database.models import (
    Expense,
    ExpenseCategory,
    Income,
    IncomeSource,
    Account,
    Person,
    session,
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


def add_expense(date, amount, account_id, category_id, notes, ctx):
    expense = Expense(
        date=date,
        amount=amount,
        account_id=account_id,
        category_id=category_id,
        notes=notes,
    )
    session.add(expense)
    session.flush()
    if expense in ctx.session_deletions["expenses"]:
        ctx.session_deletions["expenses"].remove(expense)
    else:
        ctx.session_additions["expenses"].append(expense)


def delete_expense(expense_id, ctx):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        session.delete(expense)
        session.flush()
        if expense in ctx.session_additions["expenses"]:
            ctx.session_additions["expenses"].remove(expense)
        else:
            ctx.session_deletions["expenses"].append(expense)
    else:
        logger.error(f"Expense with ID {expense_id} does not exist")


def get_expense(expense_id):
    return session.query(Expense).filter_by(id=expense_id)


def get_expenses(start_date, end_date):
    return (
        session.query(Expense)
        .filter(Expense.date >= start_date, Expense.date <= end_date)
        .all()
    )


def add_category(name, ctx):
    if session.query(ExpenseCategory).filter_by(name=name).first():
        logger.error(f"Category {name} already exists")
        return
    category = ExpenseCategory(name=name)
    session.add(category)
    session.flush()
    if category in ctx.session_deletions["categorys"]:
        ctx.session_deletions["categorys"].remove(category)
    else:
        ctx.session_additions["categorys"].append(category)


def delete_category(category_id, ctx):
    category = session.query(ExpenseCategory).filter_by(id=category_id).first()
    if category:
        session.delete(category)
        session.flush()
        if category in ctx.session_additions["categorys"]:
            ctx.session_additions["categorys"].remove(category)
        else:
            ctx.session_deletions["categorys"].append(category)
    else:
        logger.error(f"Category with ID {category_id} does not exist")


def get_category(category_id):
    return session.query(ExpenseCategory).filter_by(id=category_id).first()


def get_categories():
    return session.query(ExpenseCategory).all()


def add_income(date, amount, source_id, account_id, notes, ctx):
    income = Income(
        date=date,
        amount=amount,
        source_id=source_id,
        account_id=account_id,
        notes=notes,
    )
    session.add(income)
    session.flush()
    if income in ctx.session_deletions["incomes"]:
        ctx.session_deletions["incomes"].remove(income)
    else:
        ctx.session_additions["incomes"].append(income)


def delete_income(income_id, ctx):
    income = session.query(Income).filter_by(id=income_id).first()
    if income:
        session.delete(income)
        session.flush()
        if income in ctx.session_additions["incomes"]:
            ctx.session_additions["incomes"].remove(income)
        else:
            ctx.session_deletions["incomes"].append(income)
    else:
        logger.error(f"Income with ID {income_id} does not exist")


def get_income(income_id):
    return session.query(Income).filter_by(id=income_id).first()


def get_incomes(start_date, end_date):
    return (
        session.query(Income)
        .filter(Income.date >= start_date, Income.date <= end_date)
        .all()
    )


def add_income_source(name, ctx):
    if session.query(IncomeSource).filter_by(name=name).first():
        logger.error(f"Income source {name} already exists")
        return
    source = IncomeSource(name=name)
    session.add(source)
    session.flush()
    if source in ctx.session_deletions["sources"]:
        ctx.session_deletions["sources"].remove(source)
    else:
        ctx.session_additions["sources"].append(source)


def delete_income_source(source_id, ctx):
    source = session.query(IncomeSource).filter_by(id=source_id).first()
    if source:
        session.delete(source)
        session.flush()
        if source in ctx.session_additions["sources"]:
            ctx.session_additions["sources"].remove(source)
        else:
            ctx.session_deletions["sources"].append(source)
    else:
        logger.error(f"Income source with ID {source_id} does not exist")


def get_income_source(source_id):
    return session.query(IncomeSource).filter_by(id=source_id).first()


def get_income_sources():
    return session.query(IncomeSource).all()


def add_account(name, ctx, balance=Decimal(0)):
    if session.query(Account).filter_by(name=name).first():
        logger.error(f"Account {name} already exists")
        return
    account = Account(name=name, balance=balance)
    session.add(account)
    session.flush()
    if account in ctx.session_deletions["accounts"]:
        ctx.session_deletions["accounts"].remove(account)
    else:
        ctx.session_additions["accounts"].append(account)


def delete_account(account_id, ctx):
    account = session.query(Account).filter_by(id=account_id).first()
    if account:
        session.delete(account)
        session.flush()
        if account in ctx.session_additions["accounts"]:
            ctx.session_additions["accounts"].remove(account)
        else:
            ctx.session_deletions["accounts"].append(account)
    else:
        logger.error(f"Account with ID {account_id} does not exist")


def get_account(account_id):
    return session.query(Account).filter_by(id=account_id).first()


def get_accounts():
    return session.query(Account).all()


def add_person(name, ctx, balance=Decimal(0)):
    if session.query(Person).filter_by(name=name).first():
        logger.error(f"Person {name} already exists")
        return

    category = session.query(ExpenseCategory).filter_by(name=name).first()
    if not session.query(ExpenseCategory).filter_by(name=name).first():
        category = ExpenseCategory(name=name)
        session.add(category)
        if category in ctx.session_deletions["categorys"]:
            ctx.session_deletions["categorys"].remove(category)
        else:
            ctx.session_additions["categorys"].append(category)

    source = session.query(IncomeSource).filter_by(name=name).first()
    if not session.query(IncomeSource).filter_by(name=name).first():
        source = IncomeSource(name=name)
        session.add(source)
        if source in ctx.session_deletions["sources"]:
            ctx.session_deletions["sources"].remove(source)
        else:
            ctx.session_additions["sources"].append(source)

    session.flush()
    if category and source:
        person = Person(
            name=name, debit_id=category.id, credit_id=source.id, balance=balance
        )
        session.add(person)
        session.flush()
        if person in ctx.session_deletions["persons"]:
            ctx.session_deletions["persons"].remove(person)
        else:
            ctx.session_additions["persons"].append(person)


def delete_person(person_id, ctx):
    person = session.query(Person).filter_by(id=person_id).first()
    if person:

        session.delete(person)
        ctx.session_deletions["persons"].append(person)
        if person in ctx.session_additions["persons"]:
            ctx.session_additions["persons"].remove(person)

        category = session.query(ExpenseCategory).filter_by(id=person.debit_id).first()
        if category in ctx.session_additions["categorys"]:
            session.delete(category)
            ctx.session_additions["categorys"].remove(category)

        source = session.query(IncomeSource).filter_by(id=person.credit_id).first()
        if source in ctx.session_additions["sources"]:
            session.delete(source)
            ctx.session_additions["sources"].remove(source)

        session.flush()
    else:
        logger.error(f"Person with ID {person_id} does not exist")


def get_person(person_id):
    return session.query(Person).filter_by(id=person_id).first()


def get_persons():
    return session.query(Person).all()


def commit_changes():
    try:
        session.commit()
        logger.info("All changes have been committed successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred during commit: {e}")


def rollback_changes():
    try:
        session.rollback()
        logger.info("All uncommitted changes have been rolled back.")
    except Exception as e:
        logger.error(f"An error occurred during rollback: {e}")


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
