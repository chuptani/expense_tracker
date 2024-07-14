import logging
from decimal import Decimal

from database.models import (
    Expense,
    ExpenseCategory,
    Income,
    IncomeSource,
    Account,
    Person,
    PersonTransaction,
    session,
)

logger = logging.getLogger(__name__)


def fix_account_update_status(account, ctx):
    for entry in (
        ctx.session_additions[ctx.entry.EXPENSE]
        + ctx.session_deletions[ctx.entry.EXPENSE]
        + ctx.session_additions[ctx.entry.INCOME]
        + ctx.session_deletions[ctx.entry.INCOME]
    ):
        if account == entry.account:
            return
    ctx.session_updates[ctx.entry.ACCOUNT].remove(account)


def fix_person_update_status(person, ctx):
    for entry in (
        ctx.session_additions[ctx.entry.PERSON_TRANSACTION]
        + ctx.session_deletions[ctx.entry.PERSON_TRANSACTION]
    ):
        if person == entry.person:
            return
    ctx.session_updates[ctx.entry.PERSON].remove(person)


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
    expense.account.balance -= amount
    session.flush()
    if expense in ctx.session_deletions[ctx.entry.EXPENSE]:
        ctx.session_deletions[ctx.entry.EXPENSE].remove(expense)
    else:
        ctx.session_additions[ctx.entry.EXPENSE].append(expense)
    if expense.account not in ctx.session_updates[ctx.entry.ACCOUNT]:
        ctx.session_updates[ctx.entry.ACCOUNT].append(expense.account)
    fix_account_update_status(expense.account, ctx)


def delete_expense(expense_id, ctx):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        session.delete(expense)
        session.flush()
        expense.account.balance += expense.amount
        session.flush()
        if expense in ctx.session_additions[ctx.entry.EXPENSE]:
            ctx.session_additions[ctx.entry.EXPENSE].remove(expense)
        else:
            ctx.session_deletions[ctx.entry.EXPENSE].append(expense)
        if expense in ctx.session_updates[ctx.entry.EXPENSE]:
            ctx.session_updates[ctx.entry.EXPENSE].remove(expense)
        if expense.account not in ctx.session_updates[ctx.entry.ACCOUNT]:
            ctx.session_updates[ctx.entry.ACCOUNT].append(expense.account)
        fix_account_update_status(expense.account, ctx)
    else:
        raise ValueError(f"Expense with ID {expense_id} does not exist")


def get_expense(expense_id):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    return expense


def get_expenses(start_date, end_date):
    expenses = (
        session.query(Expense)
        .filter(Expense.date >= start_date, Expense.date <= end_date)
        .all()
    )
    return expenses


def get_all_expenses():
    expenses = session.query(Expense).all()
    return expenses


def add_category(name, ctx):
    if session.query(ExpenseCategory).filter_by(name=name).first():
        raise ValueError(f"Category '{name}' already exists")
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
        for expense in category.expenses:
            delete_expense(expense.id, ctx)
        session.delete(category)
        session.flush()
        if category in ctx.session_additions[ctx.entry.CATEGORY]:
            ctx.session_additions[ctx.entry.CATEGORY].remove(category)
        else:
            ctx.session_deletions[ctx.entry.CATEGORY].append(category)
        if category in ctx.session_updates[ctx.entry.CATEGORY]:
            ctx.session_updates[ctx.entry.CATEGORY].remove(category)
    else:
        raise ValueError(f"Category with ID {category_id} does not exist")


def get_category(category_id):
    category = session.query(ExpenseCategory).filter_by(id=category_id).first()
    return category


def get_categories():
    categories = session.query(ExpenseCategory).all()
    return categories


def add_income(date, amount, account_id, source_id, notes, ctx):
    income = Income(
        date=date,
        amount=amount,
        account_id=account_id,
        source_id=source_id,
        notes=notes,
    )
    session.add(income)
    session.flush()
    income.account.balance += amount
    session.flush()
    if income in ctx.session_deletions[ctx.entry.INCOME]:
        ctx.session_deletions[ctx.entry.INCOME].remove(income)
    else:
        ctx.session_additions[ctx.entry.INCOME].append(income)
    if income.account not in ctx.session_updates[ctx.entry.ACCOUNT]:
        ctx.session_updates[ctx.entry.ACCOUNT].append(income.account)
    fix_account_update_status(income.account, ctx)


# TODO: add account to ctx.session_updates
def delete_income(income_id, ctx):
    income = session.query(Income).filter_by(id=income_id).first()
    if income:
        session.delete(income)
        session.flush()
        income.account.balance -= income.amount
        session.flush()
        if income in ctx.session_additions[ctx.entry.INCOME]:
            ctx.session_additions[ctx.entry.INCOME].remove(income)
        else:
            ctx.session_deletions[ctx.entry.INCOME].append(income)
        if income in ctx.session_updates[ctx.entry.INCOME]:
            ctx.session_updates[ctx.entry.INCOME].remove(income)
        if income.account not in ctx.session_updates[ctx.entry.ACCOUNT]:
            ctx.session_updates[ctx.entry.ACCOUNT].append(income.account)
        fix_account_update_status(income.account, ctx)
    else:
        raise ValueError(f"Income with ID {income_id} does not exist")


def get_income(income_id):
    income = session.query(Income).filter_by(id=income_id).first()
    return income


def get_incomes(start_date, end_date):
    incomes = (
        session.query(Income)
        .filter(Income.date >= start_date, Income.date <= end_date)
        .all()
    )
    return incomes


def get_all_incomes():
    incomes = session.query(Income).all()
    return incomes


def add_source(name, ctx):
    if session.query(IncomeSource).filter_by(name=name).first():
        raise ValueError(f"Income source {name} already exists")
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
        for income in source.incomes:
            delete_income(income.id, ctx)
        session.delete(source)
        session.flush()
        if source in ctx.session_additions[ctx.entry.SOURCE]:
            ctx.session_additions[ctx.entry.SOURCE].remove(source)
        else:
            ctx.session_deletions[ctx.entry.SOURCE].append(source)
        if source in ctx.session_updates[ctx.entry.SOURCE]:
            ctx.session_updates[ctx.entry.SOURCE].remove(source)
    else:
        raise ValueError(f"Income source with ID {source_id} does not exist")


def get_source(source_id):
    source = session.query(IncomeSource).filter_by(id=source_id).first()
    return source


def get_sources():
    sources = session.query(IncomeSource).all()
    return sources


def add_account(name, ctx, balance=Decimal(0)):
    if session.query(Account).filter_by(name=name).first():
        raise ValueError(f"Account {name} already exists")
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
        for expense in account.expenses:
            delete_expense(expense.id, ctx)
        for income in account.incomes:
            delete_income(income.id, ctx)
        session.delete(account)
        session.flush()
        if account in ctx.session_additions[ctx.entry.ACCOUNT]:
            ctx.session_additions[ctx.entry.ACCOUNT].remove(account)
        else:
            ctx.session_deletions[ctx.entry.ACCOUNT].append(account)
        if account in ctx.session_updates[ctx.entry.ACCOUNT]:
            ctx.session_updates[ctx.entry.ACCOUNT].remove(account)
    else:
        raise ValueError(f"Account with ID {account_id} does not exist")


def get_account(account_id):
    account = session.query(Account).filter_by(id=account_id).first()
    return account


def get_accounts():
    accounts = session.query(Account).all()
    return accounts


def add_person(name, ctx, balance=Decimal(0)):
    name.lower().capitalize()
    person = session.query(Person).filter_by(name=name).first()
    if person:
        raise ValueError(f"Person {name} already exists")
    person = Person(name=name, balance=balance)
    session.add(person)
    session.flush()
    if person in ctx.session_deletions[ctx.entry.PERSON]:
        ctx.session_deletions[ctx.entry.PERSON].remove(person)
    else:
        ctx.session_additions[ctx.entry.PERSON].append(person)


def delete_person(person_id, ctx):
    person = session.query(Person).filter_by(id=person_id).first()
    if person:
        transactions = person.transactions
        for transaction in transactions:
            delete_person_transaction(transaction.id, ctx)
        session.delete(person)
        session.flush()
        ctx.session_deletions[ctx.entry.PERSON].append(person)
        if person in ctx.session_additions[ctx.entry.PERSON]:
            ctx.session_additions[ctx.entry.PERSON].remove(person)
        if person in ctx.session_updates[ctx.entry.PERSON]:
            ctx.session_updates[ctx.entry.PERSON].remove(person)
    else:
        raise ValueError(f"Person with ID {person_id} does not exist")


def get_person(person_id):
    person = session.query(Person).filter_by(id=person_id).first()
    return person


def get_persons():
    people = session.query(Person).all()
    return people


def add_person_transaction(date, amount, person_id, transaction_type, notes, ctx):
    person = session.query(Person).filter_by(id=person_id).first()
    if not person:
        raise ValueError(f"Person with ID {person_id} does not exist")
    transaction = PersonTransaction(
        date=date,
        amount=amount,
        person_id=person_id,
        transaction_type=transaction_type,
        notes=notes,
    )
    session.add(transaction)
    session.flush()
    person.balance += amount
    session.flush()
    if transaction in ctx.session_deletions[ctx.entry.PERSON_TRANSACTION]:
        ctx.session_deletions[ctx.entry.PERSON_TRANSACTION].remove(transaction)
    else:
        ctx.session_additions[ctx.entry.PERSON_TRANSACTION].append(transaction)
    fix_person_update_status(person, ctx)


def delete_person_transaction(transaction_id, ctx):
    transaction = session.query(PersonTransaction).filter_by(id=transaction_id).first()
    if transaction:
        person = transaction.person
        session.delete(transaction)
        session.flush()
        person.balance -= transaction.amount
        session.flush()
        if transaction in ctx.session_additions[ctx.entry.PERSON_TRANSACTION]:
            ctx.session_additions[ctx.entry.PERSON_TRANSACTION].remove(transaction)
        else:
            ctx.session_deletions[ctx.entry.PERSON_TRANSACTION].append(transaction)
        fix_person_update_status(person, ctx)
    else:
        raise ValueError(f"Person transaction with ID {transaction_id} does not exist")


def get_person_transaction(transaction_id):
    transaction = session.query(PersonTransaction).filter_by(id=transaction_id).first()
    return transaction


def get_person_transactions(start_date, end_date):
    transactions = (
        session.query(PersonTransaction)
        .filter(
            PersonTransaction.date >= start_date, PersonTransaction.date <= end_date
        )
        .all()
    )
    return transactions


# TODO: figure out logging situation


def commit_changes(ctx):
    try:
        session.commit()
        logger.info("All changes have been committed successfully.")
        all_changes = (
            ctx.session_additions.values()
            + ctx.session_deletions.values()
            + ctx.session_updates.values()
        )
        logger.info(f"Total changes: {len(all_changes)}")
        for entry in all_changes:
            logger.info(entry)

        ctx.clear_session()
    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred during commit: {e}")
        logger.error("All changes have been rolled back.")
        raise RuntimeError(f"An error occurred during commit: {e}")


def rollback_changes(ctx):
    try:
        session.rollback()
        logger.info("All uncommitted changes have been rolled back.")
        ctx.clear_session()
    except Exception as e:
        logger.error(f"An error occurred during rollback: {e}")
        raise RuntimeError(f"An error occurred during rollback: {e}")
