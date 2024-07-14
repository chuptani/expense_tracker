import os
import json
from datetime import datetime
from decimal import Decimal
from database import actions
from database.models import (
    session,
    Person,
    ExpenseCategory,
    IncomeSource,
    Expense,
    Account,
    Income,
)
from main import Ctx


ctx = Ctx(session)


def clear_database(ctx):
    expenses = session.query(Expense).all()
    categories = session.query(ExpenseCategory).all()
    incomes = session.query(Income).all()
    sources = session.query(IncomeSource).all()
    accounts = session.query(Account).all()
    people = session.query(Person).all()
    for entry in expenses + categories + incomes + sources + accounts + people:
        session.delete(entry)
    ctx.session.commit()


def repopulate_database(ctx):
    # directory = '/test_data/'
    # test_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    with open("test_data/expenses.json") as f:
        expenses = json.load(f)
    with open("test_data/categories.json") as f:
        categories = json.load(f)
    with open("test_data/incomes.json") as f:
        incomes = json.load(f)
    with open("test_data/sources.json") as f:
        sources = json.load(f)
    with open("test_data/accounts.json") as f:
        accounts = json.load(f)
    with open("test_data/people.json") as f:
        people = json.load(f)

    for category in categories:
        actions.add_category(category, ctx)

    for source in sources:
        actions.add_source(source, ctx)

    for account in accounts:
        actions.add_account(account, ctx)

    for person in people:
        actions.add_person(person, ctx)

    for expense in expenses:
        actions.add_expense(
            datetime.strptime(expense["date"], "%Y-%m-%d"),
            Decimal(expense["amount"]),
            session.query(Account).filter_by(name=expense["account"]).first().id,  # type: ignore
            session.query(ExpenseCategory).filter_by(name=expense["category"]).first().id,  # type: ignore
            expense["notes"],
            ctx,
        )

    for income in incomes:
        actions.add_income(
            datetime.strptime(income["date"], "%Y-%m-%d"),
            Decimal(income["amount"]),
            session.query(Account).filter_by(name=income["account"]).first().id,  # type: ignore
            session.query(IncomeSource).filter_by(name=income["source"]).first().id,  # type: ignore
            income["notes"],
            ctx,
        )
    ctx.session.commit()


if __name__ == "__main__":
    clear_database(ctx)
    repopulate_database(ctx)
