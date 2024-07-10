import logging
from commands import Command, CommandRegistry
from utils import utils, validation
from utils.logger import BasicFormatter, cli_logger
from database import actions

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)

# TODO: silent erros


class Add(Command):
    def __init__(self):
        super().__init__(["add", "a"], "add to database")

    def run(self, args, ctx=None):
        pass


class Entry(Command):
    def __init__(self):
        super().__init__(["entry", "e"], "add a new entry")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4):
                    entry_type, entry = validation.validate_entry_string(args, ctx)
                    if entry_type == "expense":
                        actions.add_expense(*(entry + [ctx]))
                        cli_logger.info(f"Expense '{entry[4]}' added successfully")
                        return
                    elif entry_type == "income":
                        actions.add_income(*(entry + [ctx]))
                        cli_logger.info(f"Income '{entry[4]}' added successfully")
                        return
            except ValueError as e:
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid category":
                    args[2] = validation.fix_category(args[2], ctx)
                elif str(e) == "Invalid source":
                    args[2] = validation.fix_source(args[2], ctx)
                else:
                    logger.error(e)
                    break


class Expense(Command):
    def __init__(self):
        super().__init__(["expense", "exp" "e"], "add a new expense")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4):
                    expense = validation.validate_expense_string(args, ctx)
                    actions.add_expense(*expense)
                    cli_logger.info(f"Expense '{expense[4]}' added successfully")
                    return
            except ValueError as e:
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid category":
                    args[2] = validation.fix_category(args[2], ctx)
                else:
                    logger.error(e)
                    break


class Income(Command):
    def __init__(self):
        super().__init__(["income", "inc", "i"], "add a new income")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4):
                    income = validation.validate_income_string(args, ctx)
                    actions.add_expense(*income)
                    cli_logger.info(f"Income '{income[4]}' added successfully")
                    return
            except ValueError as e:
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid source":
                    args[2] = validation.fix_source(args[2], ctx)
                else:
                    logger.error(e)
                    break


class Category(Command):
    def __init__(self):
        super().__init__(["category", "cat", "c"], "add a new category")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(args, 1)
            actions.add_category(args[0], ctx)
            cli_logger.info(f"Category '{args[0]}' added successfully")
        except ValueError as e:
            cli_logger.error(e)


class Source(Command):
    def __init__(self):
        super().__init__(["source", "sou", "s"], "add a new source")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(args, 1)
            actions.add_source(args[0], ctx)
            cli_logger.info(f"Source '{args[0]}' added successfully")
        except ValueError as e:
            cli_logger.error(e)


class Account(Command):
    def __init__(self):
        super().__init__(["account", "acc", "a"], "add a new account")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(args, 1)
            actions.add_account(args[0], ctx)
            cli_logger.info(f"Account '{args[0]}' added successfully")
        except ValueError as e:
            cli_logger.error(e)


class Person(Command):
    def __init__(self):
        super().__init__(["person", "per", "p"], "add a new person")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(args, 1)
            actions.add_person(args[0], ctx)
            cli_logger.info(f"Person '{args[0]}' added successfully")
        except ValueError as e:
            cli_logger.error(e)


add = Add()
add.add_subcommand(Entry())
add.add_subcommand(Expense())
add.add_subcommand(Category())
add.add_subcommand(Income())
add.add_subcommand(Source())
add.add_subcommand(Account())
add.add_subcommand(Person())

add_local_registery = CommandRegistry()
add_local_registery.register_command(add)


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
