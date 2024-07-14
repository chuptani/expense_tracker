import logging
from commands import Command, CommandRegistry
from utils.logger import green, yellow, red


logger = logging.getLogger(__name__)


def print_thing(thing, ctx):
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
        green(expense)
    for expense in ctx.session_deletions[thing]:
        red(expense)
    for expense in ctx.session_updates[thing]:
        yellow(expense)
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
                    red(f"invalid option {arg}")
                    continue
                if arg not in completed:
                    subcommand = self.subcommands[arg]
                    subcommand.run([], ctx)
                    completed.append(arg)
        else:
            self.run(args, ctx)

    def run(self, args, ctx):
        if not ctx.ADDITIONS and not ctx.DELETIONS and not ctx.UPDATES:
            red("No changes to display")
            return
        for thing in ctx.entry:
            print_thing(thing, ctx)


class ListExpenses(Command):
    def __init__(self):
        super().__init__(["expenses", "exp", "e"], "list all new expenses")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.EXPENSE, ctx):
            print("Expenses:")
            red("No new expenses to display")


class ListCategories(Command):
    def __init__(self):
        super().__init__(["categories", "cat", "c"], "list all new categories")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.CATEGORY, ctx):
            print("Categories:")
            red("No new categories to display")


class ListIncomes(Command):
    def __init__(self):
        super().__init__(["incomes", "inc", "i"], "list all new incomes")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.INCOME, ctx):
            print("Incomes:")
            red("No new incomes to display")


class ListSources(Command):
    def __init__(self):
        super().__init__(["sources", "src", "s"], "list all new sources")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.SOURCE, ctx):
            print("Sources:")
            red("No new sources to display")


class ListAccounts(Command):
    def __init__(self):
        super().__init__(["accounts", "acc", "a"], "list all new accounts")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.ACCOUNT, ctx):
            print("Accounts:")
            red("No new accounts to display")


class ListPersons(Command):
    def __init__(self):
        super().__init__(["persons", "per", "p"], "list all new persons")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.PERSON, ctx):
            print("Persons:")
            red("No new persons to display")


class ListPersonTransactions(Command):
    def __init__(self):
        super().__init__(
            ["person_transactions", "ptr", "pt"], "list all new person transactions"
        )

    def run(self, args, ctx):
        if not print_thing(ctx.entry.PERSON_TRANSACTION, ctx):
            print("Person Transactions:")
            red("No new person transactions to display")


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
