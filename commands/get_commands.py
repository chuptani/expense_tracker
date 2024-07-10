import inspect
from context import Entry
import logging
from commands import Command, CommandRegistry
from utils import utils
from utils.logger import BasicFormatter, cli_logger
from database import actions


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


def print_entry_for_range(entry, start_date, end_date, ctx):
    if entry == ctx.entry.EXPENSE:
        expenses = actions.get_expenses(start_date, end_date)
        print("Expenses:")
        for expense in expenses:
            print(
                f"{expense.id}. {expense.date} - {expense.amount} - {expense.account.name} - {expense.category.name} - {expense.notes}"
            )
    if entry == ctx.entry.INCOME:
        incomes = actions.get_incomes(start_date, end_date)
        print("Incomes:")
        for income in incomes:
            print(
                f"{income.id}. {income.date} - {income.amount} - {income.account.name} - {income.source.name} - {income.notes}"
            )


class Get(Command):
    def __init__(self):
        super().__init__(["get", "g"], "get things from the database")

    def run(self, args, ctx):
        cli_logger.error("No subcommand provided")


class GetExpenses(Command):
    def __init__(self):
        super().__init__(["expenses", "exp", "e"], "get expenses from the database")

    def run(self, args, ctx):
        self.subcommands["day"].run(args, ctx)


class GetIncomes(Command):
    def __init__(self):
        super().__init__(["incomes", "inc", "i"], "get incomes from the database")

    def run(self, args, ctx):
        self.subcommands["day"].run(args, ctx)


class Day(Command):
    def __init__(self, entry_type):
        self.type2str = {Entry.EXPENSE: "expense", Entry.INCOME: "income"}
        super().__init__(
            ["day", "d"], f"get {self.type2str[entry_type]}s from the current day"
        )
        self.entry_type = entry_type

    def run(self, args, ctx):
        start_date = ctx.current_date
        end_date = ctx.current_date
        print(f"{self.type2str[self.entry_type]}s for: {start_date}")
        print_entry_for_range(self.entry_type, start_date, end_date, ctx)


class Week(Command):
    def __init__(self, entry_type):
        self.type2str = {Entry.EXPENSE: "expense", Entry.INCOME: "income"}
        super().__init__(
            ["week", "w"], f"get {self.type2str[entry_type]}s from the current week"
        )
        self.entry_type = entry_type

    def run(self, args, ctx):
        start_date = ctx.this_week.start_date
        end_date = ctx.this_week.end_date
        print(f"{self.type2str[self.entry_type]}s for: {start_date} - {end_date}")
        print_entry_for_range(self.entry_type, start_date, end_date, ctx)


class Month(Command):
    def __init__(self, entry_type):
        self.type2str = {Entry.EXPENSE: "expense", Entry.INCOME: "income"}
        super().__init__(
            ["month", "m"], f"get {self.type2str[entry_type]}s from the current month"
        )
        self.entry_type = entry_type

    def run(self, args, ctx):
        start_date = ctx.this_month.start_date
        end_date = ctx.this_month.end_date
        print(f"{self.type2str[self.entry_type]}s for: {start_date} - {end_date}")
        print_entry_for_range(self.entry_type, start_date, end_date, ctx)


class Year(Command):
    def __init__(self, entry_type):
        self.type2str = {Entry.EXPENSE: "expense", Entry.INCOME: "income"}
        super().__init__(
            ["year", "y"], f"get {self.type2str[entry_type]}s from the current year"
        )
        self.entry_type = entry_type

    def run(self, args, ctx):
        start_date = ctx.this_year.start_date
        end_date = ctx.this_year.end_date
        print(f"{self.type2str[self.entry_type]}s for: {ctx.current_year.number}")
        print_entry_for_range(self.entry_type, start_date, end_date, ctx)


class range(Command):
    def __init__(self, entry_type):
        type2str = {Entry.EXPENSE: "expense", Entry.INCOME: "income"}
        super().__init__(["range", "r"], f"get {type2str[entry_type]}s in a range")
        self.entry_type = entry_type

    def run(self, args, ctx):
        try:
            utils.valid_num_of_args(args, 3)
            start_date = utils.get_date(args[1], ctx.today)
            end_date = utils.get_date(args[2], ctx.today)
        except ValueError as e:
            cli_logger.error(e)
            return
        print_entry_for_range(self.entry_type, start_date, end_date, ctx)


class GetCategories(Command):
    def __init__(self):
        super().__init__(["categories", "cat", "c"], "get categories from the database")

    def run(self, args, ctx):
        print("Categories:")
        for category in actions.get_categories():
            print(f"{category.id}. {category.name}")


class GetSources(Command):
    def __init__(self):
        super().__init__(["sources", "src", "s"], "get sources from the database")

    def run(self, args, ctx):
        print("Sources:")
        for source in actions.get_sources():
            print(f"{source.id}. {source.name}")


class GetAccounts(Command):
    def __init__(self):
        super().__init__(["accounts", "acc", "a"], "get accounts from the database")

    def run(self, args, ctx):
        print("Accounts:")
        for account in actions.get_accounts():
            print(f"{account.id}. {account.name}")


class GetPersons(Command):
    def __init__(self):
        super().__init__(["persons", "per", "p"], "get persons from the database")

    def run(self, args, ctx):
        print("Persons:")
        for person in actions.get_persons():
            print(f"{person.id}. {person.name}")


get_expenses = GetExpenses()
get_expenses.add_subcommand(range(Entry.EXPENSE))
get_expenses.add_subcommand(Day(Entry.EXPENSE))
get_expenses.add_subcommand(Week(Entry.EXPENSE))
get_expenses.add_subcommand(Month(Entry.EXPENSE))
get_expenses.add_subcommand(Year(Entry.EXPENSE))

get_income = GetIncomes()
get_income.add_subcommand(Day(Entry.INCOME))
get_income.add_subcommand(range(Entry.INCOME))
get_income.add_subcommand(Week(Entry.INCOME))
get_income.add_subcommand(Month(Entry.INCOME))
get_income.add_subcommand(Year(Entry.INCOME))

get = Get()
get.add_subcommand(get_expenses)
get.add_subcommand(GetCategories())
get.add_subcommand(get_income)
get.add_subcommand(GetSources())
get.add_subcommand(GetAccounts())
get.add_subcommand(GetPersons())

get_local_register = CommandRegistry()
get_local_register.register_command(get)


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
