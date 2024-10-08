import logging
import sys, subprocess
from commands import Command, CommandRegistry
from utils.logger import cli_logger
from database import actions

from rich.console import Console


logger = logging.getLogger(__name__)
console = Console()


class Exit(Command):
    def __init__(self):
        super().__init__(["exit", "e"], "exit the program")

    def run(self, args, ctx=None):
        sys.exit()


class Clear(Command):
    def __init__(self):
        super().__init__(["clear", "c"], "clear the screen")

    def run(self, args, ctx=None):
        subprocess.run("clear")
        return


class Commit(Command):
    def __init__(self):
        super().__init__(["commit"], "comit the current session to the database")

    def run(self, args, ctx):
        try:
            ctx.cli.execute(["ls"])
            answer = input(
                "\033[0;33mAre you sure you want to comit these changes? (Y/n): \033[0m"
            )
            if answer in ["n", "N"]:
                return
            print("Comitting session to database...")
            actions.commit_changes(ctx)
            console.print("[green]All changes have been committed successfully.")
        except Exception as e:
            logger.error(e)


class Rollback(Command):
    def __init__(self):
        super().__init__(["rollback"], "rollback the current session")

    def run(self, args, ctx):
        try:
            ctx.cli.execute(["ls"])
            answer = input(
                "\033[0;33mAre you sure you want to rollback these changes? (Y/n): \033[0m"
            )
            if answer in ["n", "N"]:
                return
            print("Rolling back changes...")
            actions.rollback_changes(ctx)
            cli_logger.info("All uncommitted changes have been rolled back")
        except Exception as e:
            logger.error(e)


class DirectAddPersonTransaction(Command):
    def __init__(self):
        super().__init__(
            ["person_transaction", "ptr", "pt"],
            "add a new person transaction",
        )

    def run(self, args, ctx):
        ctx.cli.execute(["add", "person_transaction", *args], ctx)


basic_local_registery = CommandRegistry()
basic_local_registery.register_command(Exit())
basic_local_registery.register_command(Clear())
basic_local_registery.register_command(Commit())
basic_local_registery.register_command(Rollback())


def main():
    registry = CommandRegistry()

    registry.register_command(Exit())
    registry.register_command(Clear())

    while True:
        try:
            command_line = input("> ")
            registry.execute(command_line)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
