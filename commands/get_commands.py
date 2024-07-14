import logging
from context import Entry
from commands import Command, CommandRegistry
from utils import utils
from utils.logger import cyan, red
from database import actions


logger = logging.getLogger(__name__)


def print_entry_for_range(entry, start_date, end_date, ctx):
    if entry == ctx.entry.EXPENSE:
        expenses = actions.get_expenses(start_date, end_date)
        if not expenses:
            red("No expenses to show")
        for expense in expenses:
            cyan(
                f"{expense.id}. {expense.date} - {expense.amount} - "
                f"{expense.account.name} - {expense.category.name} - {expense.notes}"
            )
    if entry == ctx.entry.INCOME:
        incomes = actions.get_incomes(start_date, end_date)
        if not incomes:
            red("No incomes to show")
        for income in incomes:
            cyan(
                f"{income.id}. {income.date} - {income.amount} - "
                f"{income.account.name} - {income.source.name} - {income.notes}"
            )
    if entry == ctx.entry.PERSON_TRANSACTION:
        transactions = actions.get_person_transactions(start_date, end_date)
        if not transactions:
            red("No transactions to show")
        for transaction in transactions:
            cyan(
                f"{transaction.id}. {transaction.date} - {transaction.amount} - "
                f"{transaction.person.name} - {transaction.transaction_type} - {transaction.notes}"
            )


type2str = {
    Entry.EXPENSE: "Expense",
    Entry.INCOME: "Income",
    Entry.PERSON_TRANSACTION: "Person Transaction",
}


class Get(Command):
    def __init__(self):
        super().__init__(["get", "g"], "get things from the database")

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
            return
        red("No subcommand provided")


class GetExpenses(Command):
    def __init__(self):
        super().__init__(["expenses", "exp", "e"], "get expenses")

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


class GetIncomes(Command):
    def __init__(self):
        super().__init__(["incomes", "inc", "i"], "get incomes")

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


class GetTransactions(Command):
    def __init__(self):
        super().__init__(["transactions", "trn", "t"], "get transactions")

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


class Day(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["day", "d"], f"from the current day")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.current_date
        end_date = ctx.current_date
        for entry_type in self.entry_types:
            print(f"{self.type2str[entry_type]}s for: {start_date}")
            print_entry_for_range(entry_type, start_date, end_date, ctx)


class Week(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["week", "w"], f"from the current week")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.this_week.start_date
        end_date = ctx.this_week.end_date
        for entry_type in self.entry_types:
            print(f"{self.type2str[entry_type]}s for: {start_date} - {end_date}")
            print_entry_for_range(entry_type, start_date, end_date, ctx)


class Month(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["month", "m"], f"from the current month")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.this_month.start_date
        end_date = ctx.this_month.end_date
        for entry_type in self.entry_types:
            print(f"{self.type2str[entry_type]}s for: {start_date} - {end_date}")
            print_entry_for_range(entry_type, start_date, end_date, ctx)


class Year(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["year", "y"], f"from the current year")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.this_year.start_date
        end_date = ctx.this_year.end_date
        for entry_type in self.entry_types:
            print(f"{self.type2str[entry_type]}s for: {ctx.current_year.number}")
            print_entry_for_range(entry_type, start_date, end_date, ctx)


class Range(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["range", "r"], f"in a range")
        self.entry_types = entry_types

    def run(self, args, ctx):
        try:
            utils.valid_num_of_args(args, 2)
            start_date = utils.get_date(args[0], ctx.today)
            end_date = utils.get_date(args[1], ctx.today)
        except ValueError as e:
            red(e)
            return
        for entry_type in self.entry_types:
            print(f"{self.type2str[entry_type]}s for: {start_date} - {end_date}")
            print_entry_for_range(entry_type, start_date, end_date, ctx)


class GetCategories(Command):
    def __init__(self):
        super().__init__(["categories", "cat", "c"], "get categories")

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        print("Categories:")
        for category in actions.get_categories():
            cyan(f"{category.id}. {category.name}")


class GetSources(Command):
    def __init__(self):
        super().__init__(["sources", "src", "s"], "get sources")

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        print("Sources:")
        for source in actions.get_sources():
            cyan(f"{source.id}. {source.name}")


class GetAccounts(Command):
    def __init__(self):
        super().__init__(["accounts", "acc", "a"], "get accounts")

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        print("Accounts:")
        for account in actions.get_accounts():
            cyan(f"{account.id}. {account.name} - {account.balance}")


class GetPersons(Command):
    def __init__(self):
        super().__init__(["persons", "per", "p"], "get persons")

    def run(self, args, ctx):
        if args:
            red(f"subcommands/arguments not expected: '{args[0]}'")
            return
        print("Persons:")
        for person in actions.get_persons():
            cyan(f"{person.id}. {person.name}")


class GetPersonTransactions(Command):
    def __init__(self):
        super().__init__(
            ["person_transactions", "ptr", "pt"], "get person transactions"
        )

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


get_expenses = GetExpenses()
get_expenses.add_subcommand(Day([Entry.EXPENSE]))
get_expenses.add_subcommand(Week([Entry.EXPENSE]))
get_expenses.add_subcommand(Month([Entry.EXPENSE]))
get_expenses.add_subcommand(Year([Entry.EXPENSE]))
get_expenses.add_subcommand(Range([Entry.EXPENSE]))

get_income = GetIncomes()
get_income.add_subcommand(Day([Entry.INCOME]))
get_income.add_subcommand(Week([Entry.INCOME]))
get_income.add_subcommand(Month([Entry.INCOME]))
get_income.add_subcommand(Year([Entry.INCOME]))
get_income.add_subcommand(Range([Entry.INCOME]))

get_transactions = GetTransactions()
get_transactions.add_subcommand(Day([Entry.EXPENSE, Entry.INCOME]))
get_transactions.add_subcommand(Week([Entry.EXPENSE, Entry.INCOME]))
get_transactions.add_subcommand(Month([Entry.EXPENSE, Entry.INCOME]))
get_transactions.add_subcommand(Year([Entry.EXPENSE, Entry.INCOME]))
get_transactions.add_subcommand(Range([Entry.EXPENSE, Entry.INCOME]))

get_person_transactions = GetPersonTransactions()
get_person_transactions.add_subcommand(Day([Entry.PERSON_TRANSACTION]))
get_person_transactions.add_subcommand(Week([Entry.PERSON_TRANSACTION]))
get_person_transactions.add_subcommand(Month([Entry.PERSON_TRANSACTION]))
get_person_transactions.add_subcommand(Year([Entry.PERSON_TRANSACTION]))
get_person_transactions.add_subcommand(Range([Entry.PERSON_TRANSACTION]))

get = Get()
get.add_subcommand(get_expenses)
get.add_subcommand(GetCategories())
get.add_subcommand(get_income)
get.add_subcommand(GetSources())
get.add_subcommand(get_transactions)
get.add_subcommand(GetAccounts())
get.add_subcommand(GetPersons())
get.add_subcommand(get_person_transactions)

get_local_registry = CommandRegistry()
get_local_registry.register_command(get)


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
