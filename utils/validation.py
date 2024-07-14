import re
from decimal import Decimal
from utils.logger import green, red
from database import actions
from utils.utils import is_number
from database.models import (
    session,
    ExpenseCategory,
    Account,
    IncomeSource,
    TransactionType,
    Person,
)


def validate_amount_string(amount):
    if is_number(amount):
        return Decimal(amount)
    raise ValueError("Invalid amount")


def validate_account_string(account):
    account = account.lower()
    if account in ["cash", "card", "s", "r"]:
        query = "cash" if account == "s" else "card" if account == "r" else account
        query_account = session.query(Account).filter_by(name=query).first()
        if query_account:
            return query_account.id
    else:
        raise ValueError("Invalid account")


def validate_category_string(category):
    query_category = session.query(ExpenseCategory).filter_by(name=category).first()
    if query_category:
        return query_category.id
    else:
        raise ValueError("Invalid category")


def validate_source_string(source):
    query_source = session.query(IncomeSource).filter_by(name=source).first()
    if query_source:
        return query_source.id
    else:
        raise ValueError("Invalid source")


def validate_expense_string(input_string, ctx):
    amount = abs(validate_amount_string(input_string[0]))
    account_id = validate_account_string(input_string[1])
    category_id = validate_category_string(input_string[2])
    notes = input_string[3]
    return [
        ctx.current_date,
        amount,
        account_id,
        category_id,
        notes,
    ]


def validate_income_string(input_string, ctx):
    amount = abs(validate_amount_string(input_string[0]))
    account_id = validate_account_string(input_string[1])
    source_id = validate_source_string(input_string[2])
    notes = input_string[3]
    return [
        ctx.current_date,
        amount,
        account_id,
        source_id,
        notes,
    ]


def entry_type(input_string, ctx=None):
    amount = input_string[0]
    if not re.match(r"^[+-]?\d+(\.\d+)?$", amount):
        raise ValueError("Invalid entry")
    if ctx:
        if is_number(amount[0]) or amount[0] == "-":
            return ctx.entry.EXPENSE
        return ctx.entry.INCOME
    else:
        return True


def validate_entry_string(input_string, ctx):
    entry = entry_type(input_string, ctx)
    if entry == ctx.entry.EXPENSE:
        return entry, validate_expense_string(input_string, ctx)
    return entry, validate_income_string(input_string, ctx)


def validate_person_string(name):
    name = name.lower().capitalize()
    person = session.query(Person).filter_by(name=name).first()
    if person:
        return person.id
    raise ValueError("Invalid person")


def validate_person_transaction_string(input_string, ctx):
    entry = entry_type(input_string, ctx)
    transaction_type = (
        TransactionType.DEBIT if entry == ctx.entry.EXPENSE else TransactionType.CREDIT
    )
    amount = abs(validate_amount_string(input_string[0]))
    person_id = validate_person_string(input_string[1])
    notes = input_string[2]
    return [
        ctx.current_date,
        amount,
        person_id,
        transaction_type,
        notes,
    ]


def validate_balance_string(input_string):
    if is_number(input_string):
        return Decimal(input_string)
    raise ValueError("Invalid balance")


def fix_account(account):
    red(f"'{account}' is not a valid account")
    while True:
        account = input("Is the transaction ca[s]h or ca[r]d? : ").lower()
        if account == "":
            pass
        elif account == "s":
            account = "cash"
            break
        elif account == "r":
            account = "card"
            break
        elif account in ["cash", "card"]:
            break
        else:
            red(f"'{account}' is not a valid account")
    green(f"Account set to '{account}'")
    return account


def fix_category(category, ctx):
    red(f"'{category}' does not exist.")
    while True:
        if category and input("Create it? [Y/n] ") in [
            "y",
            "Y",
            "",
        ]:
            actions.add_category(category, ctx)
            green(f"New category created : '{category}'")
            break
        print()
        categories = [cat.name for cat in session.query(ExpenseCategory).all()]
        print("Available categories:")
        for cat in categories:
            print(f"- {cat}")
        print()
        category = input("Enter a category: ")
        if category == "":
            continue
        if category in categories:
            green(f"Category set to '{category}'")
            break
        red(f"category '{category}' does not exist.")
    return category


def fix_source(source, ctx):
    red(f"source '{source}' does not exist.")
    while True:
        if source and input("Create it? [Y/n] ") in [
            "y",
            "Y",
            "",
        ]:
            actions.add_source(source, ctx)
            green(f"New source created : '{source}'")
            break
        sources = [src.name for src in session.query(IncomeSource).all()]
        print()
        print("Available income sources:")
        for src in sources:
            print(f"- {src}")
        print()
        source = input("Enter a source: ")
        if source == "":
            continue
        if source in sources:
            green(f"source set to '{source}'")
            break
        red(f"source '{source}' does not exist.")
    return source
