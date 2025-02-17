import logging
import database as db
from cli.context import Entry
from .commands import Command, CommandRegistry
from utils import utils
from utils.tables import ExpensesTable, IncomesTable, PersonTransactionsTable

from rich.panel import Panel
from rich.console import Console
from rich.align import Align

logger = logging.getLogger(__name__)
console = Console()


def print_entry_for_range(entry_type, start_date, end_date, caption, ctx):
    dict = {
        ctx.entry.EXPENSE: {
            "action": db.actions.get_expenses,
            "table": ExpensesTable(),
            "name": "Expenses",
        },
        ctx.entry.INCOME: {
            "action": db.actions.get_incomes,
            "table": IncomesTable(),
            "name": "Incomes",
        },
        ctx.entry.PERSON_TRANSACTION: {
            "action": db.actions.get_person_transactions,
            "table": PersonTransactionsTable(),
            "name": "Person Transactions",
        },
    }
    table = dict[entry_type]["table"]
    table.caption = caption
    entries = dict[entry_type]["action"](start_date, end_date)
    if not entries:
        console.print(
            Panel(
                Align.center(f"[red]No {dict[entry_type]["name"]} to show"),
                expand=True,
                title=dict[entry_type]["name"],
            ),
        )
        return
    for entry in entries:
        table.add_entry(entry, color="cyan")
    console.print(
        Panel(Align.center(table), expand=True, title=dict[entry_type]["name"])
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
            console.print(f"[red]invalid subcommand '{args[0]}'")
            return
        console.print("[red]No subcommand provided")


class GetExpenses(Command):
    def __init__(self):
        super().__init__(["expenses", "exp", "e"], "get expenses")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


class GetIncomes(Command):
    def __init__(self):
        super().__init__(["incomes", "inc", "i"], "get incomes")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


class GetTransactions(Command):
    def __init__(self):
        super().__init__(["transactions", "trn", "t"], "get transactions")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]invalid subcommand '{args[0]}'")
            return
        self.subcommands["day"].run(args, ctx)


class Day(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["day", "d"], f"from the current day")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.current_date
        end_date = ctx.current_date
        for entry_type in self.entry_types:
            caption = f"Day: {start_date.strftime("%b %d, %Y (%a)")}"
            print_entry_for_range(entry_type, start_date, end_date, caption, ctx)


class Week(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["week", "w"], f"from the current week")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.this_week.start_date
        end_date = ctx.this_week.end_date
        for entry_type in self.entry_types:
            caption = f"Week: {start_date.strftime("%b %d, %Y (%a)")} - {end_date.strftime("%b %d, %Y (%a)")}"
            print_entry_for_range(entry_type, start_date, end_date, caption, ctx)


class Month(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["month", "m"], f"from the current month")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.this_month.start_date
        end_date = ctx.this_month.end_date
        for entry_type in self.entry_types:
            caption = f"Month: {start_date.strftime("%B, %Y")}"
            print_entry_for_range(entry_type, start_date, end_date, caption, ctx)


class Year(Command):
    def __init__(self, entry_types):
        self.type2str = type2str
        super().__init__(["year", "y"], f"from the current year")
        self.entry_types = entry_types

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        start_date = ctx.this_year.start_date
        end_date = ctx.this_year.end_date
        for entry_type in self.entry_types:
            caption = f"Year: {ctx.current_year.number}"
            print_entry_for_range(entry_type, start_date, end_date, caption, ctx)


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
            console.print("[red]" + str(e))
            return
        for entry_type in self.entry_types:
            caption = f"{start_date} - {end_date}"
            print_entry_for_range(entry_type, start_date, end_date, caption, ctx)


class GetCategories(Command):
    def __init__(self):
        super().__init__(["categories", "cat", "c"], "get categories")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        print("Categories:")
        for category in db.actions.get_categories():
            console.print(f"[cyan]{category.id}. {category.name}")


class GetSources(Command):
    def __init__(self):
        super().__init__(["sources", "src", "s"], "get sources")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        print("Sources:")
        for source in db.actions.get_sources():
            console.print(f"[cyan]{source.id}. {source.name}")


class GetAccounts(Command):
    def __init__(self):
        super().__init__(["accounts", "acc", "a"], "get accounts")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        print("Accounts:")
        for account in db.actions.get_accounts():
            console.print(f"[cyan]{account.id}. {account.name} - {account.balance}")


class GetPersons(Command):
    def __init__(self):
        super().__init__(["persons", "per", "p"], "get persons")

    def run(self, args, ctx):
        if args:
            console.print(f"[red]subcommands/arguments not expected: '{args[0]}'")
            return
        print("Persons:")
        for person in db.actions.get_persons():
            console.print(f"[cyan]{person.id}. {person.name}")


class GetPersonTransactions(Command):
    def __init__(self):
        super().__init__(
            ["person_transactions", "ptr", "pt"], "get person transactions"
        )

    def run(self, args, ctx):
        if args:
            console.print(f"[red]invalid subcommand '{args[0]}'")
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
