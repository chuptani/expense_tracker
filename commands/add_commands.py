import logging
from decimal import Decimal
from commands import Command, CommandRegistry
from utils import utils, validation
from utils.logger import green, red
from database import actions

logger = logging.getLogger(__name__)

# TODO: args[] to dictionary


class Add(Command):
    def __init__(self):
        super().__init__(["add", "a"], "add to database")

    def run(self, args, ctx):
        if args:
            red(f"invalid subcommand '{args[0]}'")
        else:
            red("missing subcommand")


class AddEntry(Command):
    def __init__(self):
        super().__init__(["entry", "ent"], "add a new entry")

    def run(self, args, ctx):
        while True:
            try:
                if utils.valid_num_of_args(args, 4, no_args="no entry provided"):
                    entry_type, entry = validation.validate_entry_string(args, ctx)
                    if entry_type == ctx.entry.EXPENSE:
                        actions.add_expense(*(entry + [ctx]))
                        green(f"Expense '{entry[4]}' added successfully")
                        return
                    elif entry_type == ctx.entry.INCOME:
                        actions.add_income(*(entry + [ctx]))
                        green(f"Income '{entry[4]}' added successfully")
                        return
            except ValueError as e:
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid category":
                    args[2] = validation.fix_category(args[2], ctx)
                elif str(e) == "Invalid source":
                    args[2] = validation.fix_source(args[2], ctx)
                else:
                    red(e)
                    break


class AddExpense(Command):
    def __init__(self):
        super().__init__(["expense", "exp", "e"], "add a new expense")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4, no_args="no expense provided"):
                    expense = validation.validate_expense_string(args, ctx)
                    actions.add_expense(*(expense + [ctx]))
                    green(f"Expense '{expense[4]}' added successfully")
                    return
            except ValueError as e:
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid category":
                    args[2] = validation.fix_category(args[2], ctx)
                else:
                    red(e)
                    logger.error(e)
                    break


class AddIncome(Command):
    def __init__(self):
        super().__init__(["income", "inc", "i"], "add a new income")

    def run(self, args, ctx=None):
        while True:
            try:
                if utils.valid_num_of_args(args, 4, no_args="no income provided"):
                    income = validation.validate_income_string(args, ctx)
                    actions.add_income(*(income + [ctx]))
                    green(f"Income '{income[4]}' added successfully")
                    return
            except ValueError as e:
                if str(e) == "Invalid account":
                    args[1] = validation.fix_account(args[1])
                elif str(e) == "Invalid source":
                    args[2] = validation.fix_source(args[2], ctx)
                else:
                    red(e)
                    break


class AddCategory(Command):
    def __init__(self):
        super().__init__(["category", "cat", "c"], "add a new category")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(
                args,
                1,
                no_args="no category name provided",
                extra_args=f"subcommands/arguments not expected: '{utils.if_args_get_arg(args, 1)}'",
            )
            category_name = args[0]
            actions.add_category(category_name, ctx)
            green(f"Category '{category_name}' added successfully")
        except ValueError as e:
            red(e)


class AddSource(Command):
    def __init__(self):
        super().__init__(["source", "src", "s"], "add a new source")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(
                args,
                1,
                no_args="no source name provided",
                extra_args=f"subcommands/arguments not expected: '{utils.if_args_get_arg(args, 1)}'",
            )
            source_name = args[0]
            actions.add_source(source_name, ctx)
            green(f"Source '{source_name}' added successfully")
        except ValueError as e:
            red(e)


class AddAccount(Command):
    def __init__(self):
        super().__init__(["account", "acc", "a"], "add a new account")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(
                args,
                2,
                no_args="no account provided",
                extra_args=f"subcommands/arguments not expected: '{utils.if_args_get_arg(args, 2)}'",
            )
            account_name = args[0]
            if len(args) == 2:
                balance = validation.validate_balance_string(args[1])
            else:
                balance = Decimal(0)

            actions.add_account(account_name, ctx, balance)
            green(f"Account '{account_name}' added successfully")
        except ValueError as e:
            red(e)


class AddPerson(Command):
    def __init__(self):
        super().__init__(["person", "per", "p"], "add a new person")

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(
                args,
                2,
                no_args="no person provided",
                extra_args=f"subcommands/arguments not expected: '{utils.if_args_get_arg(args, 2)}'",
            )
            person_name = args[0]
            if len(args) == 2:
                balance = validation.validate_balance_string(args[1])
            else:
                balance = Decimal(0)
            actions.add_person(person_name, ctx, balance)
            green(f"Person '{person_name}' added successfully")
        except ValueError as e:
            red(e)


class AddPersonTransaction(Command):
    def __init__(self):
        super().__init__(
            ["person_transaction", "ptr", "pt"], "add a new person transaction"
        )

    def run(self, args, ctx=None):
        try:
            utils.valid_num_of_args(args, 3, no_args="no person transaction provided")
            person_name = args[0]
            transaction = validation.validate_person_transaction_string(args, ctx)
            person_name = person_name.lower().capitalize()
            actions.add_person_transaction(*(transaction + [ctx]))
            green(f"Person Transaction '{person_name}' added successfully")
        except ValueError as e:
            red(e)


add = Add()
add.add_subcommand(AddEntry())
add.add_subcommand(AddExpense())
add.add_subcommand(AddCategory())
add.add_subcommand(AddIncome())
add.add_subcommand(AddSource())
add.add_subcommand(AddAccount())
add.add_subcommand(AddPerson())
add.add_subcommand(AddPersonTransaction())

add_local_registery = CommandRegistry()
add_local_registery.register_command(add)
add_local_registery.register_command(AddPersonTransaction())


def main():
    while True:
        try:
            command_line = input("> ")
            add_local_registery.execute(command_line)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
