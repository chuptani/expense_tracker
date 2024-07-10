import logging
from commands import Command, CommandRegistry
from utils.logger import BasicFormatter, cli_logger


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


def print_thing(thing, ctx):
    if not any(
        value
        for value in ctx.session_additions[thing]
        + ctx.session_deletions[thing]
        + ctx.session_updates[thing]
    ):
        return False
    print("Expenses:")
    for expense in ctx.session_additions[thing]:
        cli_logger.info(expense)
    for expense in ctx.session_deletions[thing]:
        cli_logger.error(expense)
    for expense in ctx.session_updates[thing]:
        cli_logger.warning(expense)
    return True


class List(Command):
    def __init__(self):
        super().__init__(["list", "ls"], "list all new entries")

    def execute(self, args, ctx):
        if args and args[0] == "help":
            print(self.help(), end="")
        elif args:
            for arg in args:
                if arg not in self.subcommands:
                    logger.error(f"invalid option {arg}")
                    return
                subcommand = self.subcommands[arg]
                subcommand.run([], ctx)
        else:
            self.run(args, ctx)

    def run(self, args, ctx):

        if not ctx.ADDITIONS and not ctx.DELETIONS and not ctx.UPDATES:
            cli_logger.error("No changes to display")
            return

        for thing in ctx.entry:
            print_thing(thing, ctx)


class ListExpenses(Command):
    def __init__(self):
        super().__init__(["expenses", "e"], "list all new expenses")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.EXPENSE, ctx):
            print("Expenses:")
            cli_logger.error("No new expenses to display")


class ListCategories(Command):
    def __init__(self):
        super().__init__(["categories", "c"], "list all new categories")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.CATEGORY, ctx):
            print("Categories:")
            cli_logger.error("No new categories to display")


class ListIncomes(Command):
    def __init__(self):
        super().__init__(["incomes", "i"], "list all new incomes")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.INCOME, ctx):
            print("Incomes:")
            cli_logger.error("No new incomes to display")


class ListSources(Command):
    def __init__(self):
        super().__init__(["sources", "s"], "list all new sources")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.SOURCE, ctx):
            print("Sources:")
            cli_logger.error("No new sources to display")


class ListAccounts(Command):
    def __init__(self):
        super().__init__(["accounts", "a"], "list all new accounts")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.ACCOUNT, ctx):
            print("Accounts:")
            cli_logger.error("No new accounts to display")


class ListPersons(Command):
    def __init__(self):
        super().__init__(["persons", "p"], "list all new persons")

    def run(self, args, ctx):
        if not print_thing(ctx.entry.PERSON, ctx):
            print("Persons:")
            cli_logger.error("No new persons to display")


ls = List()
ls.add_subcommand(ListExpenses())
ls.add_subcommand(ListCategories())
ls.add_subcommand(ListIncomes())
ls.add_subcommand(ListSources())
ls.add_subcommand(ListAccounts())
ls.add_subcommand(ListPersons())

list_local_registery = CommandRegistry()
list_local_registery.register_command(ls)


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
