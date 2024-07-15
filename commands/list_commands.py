import logging

from commands import Command, CommandRegistry
from utils.tables import (
    ExpensesTable,
    CategoriesTable,
    IncomesTable,
    SourcesTable,
    AccountsTable,
    PersonsTable,
    PersonTransactionsTable,
)

from rich.console import Console
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.align import Align

logger = logging.getLogger(__name__)

console = Console()


def get_table(thing, ctx):
    things = {
        ctx.entry.EXPENSE: {"title": "Expenses", "table": ExpensesTable()},
        ctx.entry.CATEGORY: {"title": "Categories", "table": CategoriesTable()},
        ctx.entry.INCOME: {"title": "Incomes", "table": IncomesTable()},
        ctx.entry.SOURCE: {"title": "Sources", "table": SourcesTable()},
        ctx.entry.ACCOUNT: {"title": "Accounts", "table": AccountsTable()},
        ctx.entry.PERSON: {"title": "Persons", "table": PersonsTable()},
        ctx.entry.PERSON_TRANSACTION: {
            "title": "Person Transactions",
            "table": PersonTransactionsTable(),
        },
    }

    thingfo = things[thing]
    table = thingfo["table"]

    if not any(
        value
        for value in ctx.session_additions[thing]
        + ctx.session_deletions[thing]
        + ctx.session_updates[thing]
    ):
        return Panel(
            Align.center(f"[red]No {thingfo["title"]} to show"),
            # padding=1,
            title=f"{thingfo["title"]}",
            expand=True,
        )

    for entry in ctx.session_additions[thing]:
        table.add_entry(entry, "green")
    for entry in ctx.session_deletions[thing]:
        table.add_entry(entry, "red")
    for entry in ctx.session_updates[thing]:
        table.add_entry(entry, "yellow")

    return Panel(Align.center(table), title=f"{thingfo["title"]}", expand=True)


def old_print_thing(thing, ctx):
    things = {
        ctx.entry.EXPENSE: "Expenses",
        ctx.entry.CATEGORY: "Categories",
        ctx.entry.INCOME: "Incomes",
        ctx.entry.SOURCE: "Sources",
        ctx.entry.ACCOUNT: "Accounts",
        ctx.entry.PERSON: "Persons",
        ctx.entry.PERSON_TRANSACTION: "Person Transactions",
    }

    if not any(
        value
        for value in ctx.session_additions[thing]
        + ctx.session_deletions[thing]
        + ctx.session_updates[thing]
    ):
        return False

    print(things[thing] + ":")
    for expense in ctx.session_additions[thing]:
        console.print("[green]" + str(expense))
    for expense in ctx.session_deletions[thing]:
        console.print("[red]" + str(expense))
    for expense in ctx.session_updates[thing]:
        console.print("[yellow]" + str(expense))
    return True


class List(Command):
    def __init__(self):
        super().__init__(["list", "ls"], "list all new entries")

    def execute(self, args, ctx):
        if args and args[0] == "help":
            print(self.help(), end="")
        elif args:
            completed = []
            for arg in args:
                if arg not in self.subcommands:
                    console.print(f"[red]invalid option: '{arg}'")
                    continue
                if arg not in completed:
                    subcommand = self.subcommands[arg]
                    subcommand.run([], ctx)
                    completed.append(arg)
        else:
            self.run(args, ctx)

    def run(self, args, ctx):
        # for thing in ctx.entry:
        #     old_print_thing(thing, ctx)
        renderables = [get_table(thing, ctx) for thing in ctx.entry]
        row_1 = Columns(renderables[:2], expand=True)
        row_2 = Columns(renderables[3:1:-1], expand=True)
        row_3 = Columns(renderables[4:5], expand=True)
        row_4 = Columns(renderables[5:], expand=True)
        group = Group(row_1, row_2, row_3, row_4)
        console.print(Panel(group))


class ListExpenses(Command):
    def __init__(self):
        super().__init__(["expenses", "exp", "e"], "list all new expenses")

    def run(self, args, ctx):
        table = get_table(ctx.entry.EXPENSE, ctx)
        console.print(table)


class ListCategories(Command):
    def __init__(self):
        super().__init__(["categories", "cat", "c"], "list all new categories")

    def run(self, args, ctx):
        table = get_table(ctx.entry.CATEGORY, ctx)
        console.print(table)


class ListIncomes(Command):
    def __init__(self):
        super().__init__(["incomes", "inc", "i"], "list all new incomes")

    def run(self, args, ctx):
        table = get_table(ctx.entry.INCOME, ctx)
        console.print(table)


class ListSources(Command):
    def __init__(self):
        super().__init__(["sources", "src", "s"], "list all new sources")

    def run(self, args, ctx):
        table = get_table(ctx.entry.SOURCE, ctx)
        console.print(table)


class ListAccounts(Command):
    def __init__(self):
        super().__init__(["accounts", "acc", "a"], "list all new accounts")

    def run(self, args, ctx):
        table = get_table(ctx.entry.ACCOUNT, ctx)
        console.print(table)


class ListPersons(Command):
    def __init__(self):
        super().__init__(["persons", "per", "p"], "list all new persons")

    def run(self, args, ctx):
        table = get_table(ctx.entry.PERSON, ctx)
        console.print(table)


class ListPersonTransactions(Command):
    def __init__(self):
        super().__init__(
            ["person_transactions", "ptr", "pt"], "list all new person transactions"
        )

    def run(self, args, ctx):
        table = get_table(ctx.entry.PERSON_TRANSACTION, ctx)
        console.print(table)


ls = List()
ls.add_subcommand(ListExpenses())
ls.add_subcommand(ListCategories())
ls.add_subcommand(ListIncomes())
ls.add_subcommand(ListSources())
ls.add_subcommand(ListAccounts())
ls.add_subcommand(ListPersons())
ls.add_subcommand(ListPersonTransactions())

list_local_registery = CommandRegistry()
list_local_registery.register_command(ls)


def main():
    while True:
        try:
            command_line = input("> ")
            list_local_registery.execute(command_line)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
