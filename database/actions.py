import logging

from sqlalchemy import ExecutionContext
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
# handler = logging.StreamHandler()
# handler.setFormatter(BasicFormatter())
# logger.addHandler(handler)


def add_expense(date, amount, account_id, category_id, notes, ctx):
    expense = Expense(
        date=date,
        amount=amount,
        account_id=account_id,
        category_id=category_id,
        notes=notes,
    )
    session.add(expense)
    expense.account.balance -= amount
    session.flush()
    if expense in ctx.session_deletions[ctx.entry.EXPENSE]:
        ctx.session_deletions[ctx.entry.EXPENSE].remove(expense)
    else:
        ctx.session_additions[ctx.entry.EXPENSE].append(expense)


def delete_expense(expense_id, ctx):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        session.delete(expense)
        expense.account.balance += expense.amount
        session.flush()
        if expense in ctx.session_additions[ctx.entry.EXPENSE]:
            ctx.session_additions[ctx.entry.EXPENSE].remove(expense)
        else:
            ctx.session_deletions[ctx.entry.EXPENSE].append(expense)
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
    if category in ctx.session_deletions[ctx.entry.CATEGORY]:
        ctx.session_deletions[ctx.entry.CATEGORY].remove(category)
    else:
        ctx.session_additions[ctx.entry.CATEGORY].append(category)


def delete_category(category_id, ctx):
    category = session.query(ExpenseCategory).filter_by(id=category_id).first()
    if category:
        session.delete(category)
        session.flush()
        if category in ctx.session_additions[ctx.entry.CATEGORY]:
            ctx.session_additions[ctx.entry.CATEGORY].remove(category)
        else:
            ctx.session_deletions[ctx.entry.CATEGORY].append(category)
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
    income.account.balance += amount
    session.flush()
    if income in ctx.session_deletions[ctx.entry.INCOME]:
        ctx.session_deletions[ctx.entry.INCOME].remove(income)
    else:
        ctx.session_additions[ctx.entry.INCOME].append(income)


def delete_income(income_id, ctx):
    income = session.query(Income).filter_by(id=income_id).first()
    if income:
        session.delete(income)
        income.account.balance -= income.amount
        session.flush()
        if income in ctx.session_additions[ctx.entry.INCOME]:
            ctx.session_additions[ctx.entry.INCOME].remove(income)
        else:
            ctx.session_deletions[ctx.entry.INCOME].append(income)
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


def add_source(name, ctx):
    if session.query(IncomeSource).filter_by(name=name).first():
        logger.error(f"Income source {name} already exists")
        return
    source = IncomeSource(name=name)
    session.add(source)
    session.flush()
    if source in ctx.session_deletions[ctx.entry.SOURCE]:
        ctx.session_deletions[ctx.entry.SOURCE].remove(source)
    else:
        ctx.session_additions[ctx.entry.SOURCE].append(source)


def delete_source(source_id, ctx):
    source = session.query(IncomeSource).filter_by(id=source_id).first()
    if source:
        session.delete(source)
        session.flush()
        if source in ctx.session_additions[ctx.entry.SOURCE]:
            ctx.session_additions[ctx.entry.SOURCE].remove(source)
        else:
            ctx.session_deletions[ctx.entry.SOURCE].append(source)
    else:
        logger.error(f"Income source with ID {source_id} does not exist")


def get_source(source_id):
    return session.query(IncomeSource).filter_by(id=source_id).first()


def get_sources():
    return session.query(IncomeSource).all()


def add_account(name, ctx, balance=Decimal(0)):
    if session.query(Account).filter_by(name=name).first():
        logger.error(f"Account {name} already exists")
        return
    account = Account(name=name, balance=balance)
    session.add(account)
    session.flush()
    if account in ctx.session_deletions[ctx.entry.ACCOUNT]:
        ctx.session_deletions[ctx.entry.ACCOUNT].remove(account)
    else:
        ctx.session_additions[ctx.entry.ACCOUNT].append(account)


def delete_account(account_id, ctx):
    account = session.query(Account).filter_by(id=account_id).first()
    if account:
        session.delete(account)
        session.flush()
        if account in ctx.session_additions[ctx.entry.ACCOUNT]:
            ctx.session_additions[ctx.entry.ACCOUNT].remove(account)
        else:
            ctx.session_deletions[ctx.entry.ACCOUNT].append(account)
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
        if category in ctx.session_deletions[ctx.entry.CATEGORY]:
            ctx.session_deletions[ctx.entry.CATEGORY].remove(category)
        else:
            ctx.session_additions[ctx.entry.CATEGORY].append(category)

    source = session.query(IncomeSource).filter_by(name=name).first()
    if not session.query(IncomeSource).filter_by(name=name).first():
        source = IncomeSource(name=name)
        session.add(source)
        if source in ctx.session_deletions[ctx.entry.SOURCE]:
            ctx.session_deletions[ctx.entry.SOURCE].remove(source)
        else:
            ctx.session_additions[ctx.entry.SOURCE].append(source)

    session.flush()
    if category and source:
        person = Person(
            name=name, debit_id=category.id, credit_id=source.id, balance=balance
        )
        session.add(person)
        session.flush()
        if person in ctx.session_deletions[ctx.entry.PERSON]:
            ctx.session_deletions[ctx.entry.PERSON].remove(person)
        else:
            ctx.session_additions[ctx.entry.PERSON].append(person)


def delete_person(person_id, ctx):
    person = session.query(Person).filter_by(id=person_id).first()
    if person:

        session.delete(person)
        ctx.session_deletions[ctx.entry.PERSON].append(person)
        if person in ctx.session_additions[ctx.entry.PERSON]:
            ctx.session_additions[ctx.entry.PERSON].remove(person)

        category = session.query(ExpenseCategory).filter_by(id=person.debit_id).first()
        if category in ctx.session_additions[ctx.entry.CATEGORY]:
            session.delete(category)
            ctx.session_additions[ctx.entry.CATEGORY].remove(category)

        source = session.query(IncomeSource).filter_by(id=person.credit_id).first()
        if source in ctx.session_additions[ctx.entry.SOURCE]:
            session.delete(source)
            ctx.session_additions[ctx.entry.SOURCE].remove(source)

        session.flush()
    else:
        logger.error(f"Person with ID {person_id} does not exist")


def get_person(person_id):
    return session.query(Person).filter_by(id=person_id).first()


def get_persons():
    return session.query(Person).all()


# TODO: figure out logging situation


def commit_changes(ctx):
    try:
        session.commit()
        ctx.clear_session()
        # logger.info("All changes have been committed successfully.")
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"An error occurred during commit: {e}")


def rollback_changes(ctx):
    try:
        session.rollback()
        ctx.clear_session()
        # logger.info("All uncommitted changes have been rolled back.")
    except Exception as e:
        raise RuntimeError(f"An error occurred during rollback: {e}")


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
