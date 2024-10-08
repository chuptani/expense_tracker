import logging
from commands import Command, CommandRegistry
from utils import utils
from utils.logger import green, red
import database as db


logger = logging.getLogger(__name__)


def delete_things(entry_type, args, ctx):
    type2str = {
        ctx.entry.EXPENSE: "expense",
        ctx.entry.INCOME: "income",
        ctx.entry.CATEGORY: "category",
        ctx.entry.SOURCE: "source",
        ctx.entry.ACCOUNT: "account",
        ctx.entry.PERSON: "person",
        ctx.entry.PERSON_TRANSACTION: "person_transaction",
    }
    thing = type2str[entry_type]
    thing_ids = args
    valid_thing_ids = []
    for thing_id in thing_ids:
        try:
            if not utils.is_number(thing_id):
                red(f"invalid {thing} id '{thing_id}'")
                continue
            entry = None
            if entry_type == ctx.entry.EXPENSE:
                entry = db.actions.get_expense(thing_id)
            elif entry_type == ctx.entry.INCOME:
                entry = db.actions.get_income(thing_id)
            elif entry_type == ctx.entry.CATEGORY:
                entry = db.actions.get_category(thing_id)
            elif entry_type == ctx.entry.SOURCE:
                entry = db.actions.get_source(thing_id)
            elif entry_type == ctx.entry.ACCOUNT:
                entry = db.actions.get_account(thing_id)
            elif entry_type == ctx.entry.PERSON:
                entry = db.actions.get_person(thing_id)
            elif entry_type == ctx.entry.PERSON_TRANSACTION:
                entry = db.actions.get_person_transaction(thing_id)
            if not entry:
                red(f"{thing} '{thing_id}' not found")
                continue
            red(entry)
            valid_thing_ids.append(thing_id)
        except ValueError as e:
            red(e)
    if not valid_thing_ids:
        red("Nothing to delete")
        return
    if input(f"\033[0;33mDelete these {thing}s? [Y/n] \033[0m") in ["n", "N"]:
        return
    for thing_id in valid_thing_ids:
        if entry_type == ctx.entry.EXPENSE:
            db.actions.delete_expense(thing_id, ctx)
        elif entry_type == ctx.entry.INCOME:
            db.actions.delete_income(thing_id, ctx)
        elif entry_type == ctx.entry.CATEGORY:
            db.actions.delete_category(thing_id, ctx)
        elif entry_type == ctx.entry.SOURCE:
            db.actions.delete_source(thing_id, ctx)
        elif entry_type == ctx.entry.ACCOUNT:
            db.actions.delete_account(thing_id, ctx)
        elif entry_type == ctx.entry.PERSON:
            db.actions.delete_person(thing_id, ctx)
        elif entry_type == ctx.entry.PERSON_TRANSACTION:
            db.actions.delete_person_transaction(thing_id, ctx)
        green(f"{thing} '{thing_id}' deleted")


class Delete(Command):
    def __init__(self):
        super().__init__(["delete", "del"], "delete things from the database")

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
            return
        red("No subcommand provided")


class DeleteExpense(Command):
    def __init__(self):
        super().__init__(["expense", "exp", "e"], "delete expenses")

    def run(self, args, ctx):
        expense_ids = args
        valid_expense_ids = []
        for expense_id in expense_ids:
            try:
                if not utils.is_number(expense_id):
                    red(f"invalid expense id '{expense_id}'")
                    continue
                expense = db.actions.get_expense(expense_id)
                if not expense:
                    red(f"expense {expense_id} not found")
                    continue
                red(expense)
                valid_expense_ids.append(expense_id)
            except ValueError as e:
                red(e)
        if not valid_expense_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these expenses? [Y/n] \033[0m") in ["n", "N"]:
            return
        for expense_id in valid_expense_ids:
            db.actions.delete_expense(expense_id, ctx)
            green(f"expense {expense_id} deleted")


class DeleteIncome(Command):
    def __init__(self):
        super().__init__(["income", "inc", "i"], "delete incomes")

    def run(self, args, ctx):
        income_ids = args
        valid_income_ids = []
        for income_id in income_ids:
            try:
                if not utils.is_number(income_id):
                    red(f"invalid income id '{income_id}'")
                    continue
                income = db.actions.get_income(income_id)
                if not income:
                    red(f"income {income_id} not found")
                    continue
                red(income)
                valid_income_ids.append(income_id)
            except ValueError as e:
                red(e)
        if not valid_income_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these incomes? [Y/n] \033[0m") in ["n", "N"]:
            return
        for income_id in valid_income_ids:
            db.actions.delete_income(income_id, ctx)
            green(f"income {income_id} deleted")


class DeleteCategory(Command):
    def __init__(self):
        super().__init__(["category", "cat", "c"], "delete categories")

    def run(self, args, ctx):
        category_ids = args
        valid_category_ids = []
        for category_id in category_ids:
            try:
                if not utils.is_number(category_id):
                    red(f"invalid category id '{category_id}'")
                    continue
                category = db.actions.get_category(category_id)
                if not category:
                    red(f"category {category_id} not found")
                    continue
                red(category)
                valid_category_ids.append(category_id)
            except ValueError as e:
                red(e)
        if not valid_category_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these categories? [Y/n] \033[0m") in ["n", "N"]:
            return
        for category_id in valid_category_ids:
            db.actions.delete_category(category_id, ctx)
            green(f"category {category_id} deleted")


class DeleteSource(Command):
    def __init__(self):
        super().__init__(["source", "src", "s"], "delete sources")

    def run(self, args, ctx):
        source_ids = args
        valid_source_ids = []
        for source_id in source_ids:
            try:
                if not utils.is_number(source_id):
                    red(f"invalid source id '{source_id}'")
                    continue
                source = db.actions.get_source(source_id)
                if not source:
                    red(f"source {source_id} not found")
                    continue
                red(source)
                valid_source_ids.append(source_id)
            except ValueError as e:
                red(e)
        if not valid_source_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these sources? [Y/n] \033[0m") in ["n", "N"]:
            return
        for source_id in valid_source_ids:
            db.actions.delete_source(source_id, ctx)
            green(f"source {source_id} deleted")


class DeletePerson(Command):
    def __init__(self):
        super().__init__(["person", "per", "p"], "delete persons")

    def run(self, args, ctx):
        person_ids = args
        valid_person_ids = []
        for person_id in person_ids:
            try:
                if not utils.is_number(person_id):
                    red(f"invalid person id '{person_id}'")
                    continue
                person = db.actions.get_person(person_id)
                if not person:
                    red(f"person {person_id} not found")
                    continue
                red(person)
                valid_person_ids.append(person_id)
            except ValueError as e:
                red(e)
        if not valid_person_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these persons? [Y/n] \033[0m") in ["n", "N"]:
            return
        for person_id in valid_person_ids:
            db.actions.delete_person(person_id, ctx)
            green(f"person {person_id} deleted")


class DeletePersonTransaction(Command):
    def __init__(self):
        super().__init__(
            ["person_transaction", "ptr", "pt"], "delete person transactions"
        )

    def run(self, args, ctx):
        person_transaction_ids = args
        valid_person_transaction_ids = []
        for person_transaction_id in person_transaction_ids:
            try:
                if not utils.is_number(person_transaction_id):
                    red(f"invalid person transaction id '{person_transaction_id}'")
                    continue
                person_transaction = db.actions.get_person_transaction(
                    person_transaction_id
                )
                if not person_transaction:
                    red(f"person transaction {person_transaction_id} not found")
                    continue
                red(person_transaction)
                valid_person_transaction_ids.append(person_transaction_id)
            except ValueError as e:
                red(e)
        if not valid_person_transaction_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these person transactions? [Y/n] \033[0m") in [
            "n",
            "N",
        ]:
            return
        for person_transaction_id in valid_person_transaction_ids:
            db.actions.delete_person_transaction(person_transaction_id, ctx)
            green(f"person transaction {person_transaction_id} deleted")


class DeleteAccount(Command):
    def __init__(self):
        super().__init__(["account", "acc", "a"], "delete accounts")

    def run(self, args, ctx):
        account_ids = args
        valid_account_ids = []
        for account_id in account_ids:
            try:
                if not utils.is_number(account_id):
                    red(f"invalid account id '{account_id}'")
                    continue
                account = db.actions.get_account(account_id)
                if not account:
                    red(f"account {account_id} not found")
                    continue
                red(account)
                valid_account_ids.append(account_id)
            except ValueError as e:
                red(e)
        if not valid_account_ids:
            red("Nothing to delete")
            return
        if input("\033[0;33mDelete these accounts? [Y/n] \033[0m") in ["n", "N"]:
            return
        for account_id in valid_account_ids:
            db.actions.delete_account(account_id, ctx)
            green(f"account {account_id} deleted")


delete = Delete()
delete.add_subcommand(DeleteExpense())
delete.add_subcommand(DeleteCategory())
delete.add_subcommand(DeleteIncome())
delete.add_subcommand(DeleteSource())
delete.add_subcommand(DeleteAccount())
delete.add_subcommand(DeletePerson())
delete.add_subcommand(DeletePersonTransaction())

delete_local_registry = CommandRegistry()
delete_local_registry.register_command(delete)


def main():
    registry = CommandRegistry()

    while True:
        try:
            command_line = input("> ")
            registry.execute(command_line)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
