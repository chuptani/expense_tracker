import re
from decimal import Decimal
from utils.logger import cli_logger
from database import actions
from utils.utils import is_number
from database.models import session, ExpenseCategory, Account, IncomeSource


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
        cli_logger.error(f"'{account}' is not a valid account")
        raise ValueError("Invalid account")


def validate_category_string(category):
    query_category = session.query(ExpenseCategory).filter_by(name=category).first()
    if query_category:
        return query_category.id
    else:
        cli_logger.error(f"'{category}' category does not exist.")
        raise ValueError("Invalid category")


def validate_source_string(source):
    query_source = session.query(IncomeSource).filter_by(name=source).first()
    if query_source:
        return query_source.id
    else:
        cli_logger.error(f"'{source}' source does not exist.")
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


def entry_type(input_string):
    amount = input_string[0]
    if not re.match(r"^[+-]?\d+(\.\d+)?$", amount):
        raise ValueError("Invalid entry")
    if is_number(amount[0]) or amount[0] == "-":
        return "expense"
    return "income"


def validate_entry_string(input_string, ctx):
    entry = entry_type(input_string)
    if entry == "expense":
        return entry, validate_expense_string(input_string, ctx)
    return entry, validate_income_string(input_string, ctx)


def fix_account(account):
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
            cli_logger.error(f"'{account}' is not a valid account")
    cli_logger.info(f"Account set to '{account}'")
    return account


def fix_category(category, ctx):
    while True:
        if category and input("Create it? [Y/n] ") in [
            "y",
            "Y",
            "",
        ]:
            actions.add_category(category, ctx)
            cli_logger.info(f"New category created : '{category}'")
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
            cli_logger.info(f"Category set to '{category}'")
            break
        cli_logger.error(f"'{category}' category does not exist.")
    return category


def fix_source(source, ctx):
    while True:
        if source and input("Create it? [Y/n] ") in [
            "y",
            "Y",
            "",
        ]:
            actions.add_income_source(source, ctx)
            cli_logger.info(f"New source created : '{source}'")
            break
        sources = [sou.name for sou in session.query(IncomeSource).all()]
        print()
        print("Available income sources:")
        for sou in sources:
            print(f"- {sou}")
        print()
        source = input("Enter a source: ")
        if source == "":
            continue
        if source in sources:
            cli_logger.info(f"source set to '{source}'")
            break
        cli_logger.error(f"'{source}' source does not exist.")
    return source
