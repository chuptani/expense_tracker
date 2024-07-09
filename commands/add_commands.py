import logging
from commands import Command, CommandRegistry
from utils import utils, validation
from utils.logger import BasicFormatter, cli_logger
from database import actions

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


class Add(Command):
    def __init__(self):
        super().__init__(["add", "a"], "add to database")

    def run(self, args, ctx=None):
        pass


class Account(Command):
    def __init__(self):
        super().__init__(["account", "a"], "add a new account")

    def run(self, args, ctx=None):
        logger.warning("command not defined")


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
                # TODO: silent erros
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
        super().__init__(["expense", "e"], "add a new expense")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4):
                    expense = validation.validate_expense_string(args, ctx)
                    actions.add_expense(*expense)
                    cli_logger.info(f"Expense '{expense[4]}' added successfully")
                    return
            except ValueError as e:
                # TODO: silent erros
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid category":
                    args[2] = validation.fix_category(args[2], ctx)
                else:
                    logger.error(e)
                    break


class Income(Command):
    def __init__(self):
        super().__init__(["income", "i"], "add a new income")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4):
                    income = validation.validate_income_string(args, ctx)
                    actions.add_expense(*income)
                    cli_logger.info(f"Income '{income[4]}' added successfully")
                    return
            except ValueError as e:
                # TODO: silent erros
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid source":
                    args[2] = validation.fix_source(args[2], ctx)
                else:
                    logger.error(e)
                    break


add = Add()
add.add_subcommand(Account())
add.add_subcommand(Entry())
add.add_subcommand(Expense())
add.add_subcommand(Income())

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
