import logging
import sys, subprocess
from commands import Command, CommandRegistry
from utils import utils
from utils.logger import BasicFormatter, cli_logger


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


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


class Entry(Command):
    def __init__(self):
        super().__init__(
            ["entry"],
            "add a new entry (if no command is passed new entry is assumed)",
        )

    def run(self, args, ctx=None):
        if not utils.valid_num_of_args(args, 4, "entry:"):
            return
        else:
            print(utils.valid_entry(args, ctx))


class Commit(Command):
    def __init__(self):
        super().__init__(["commit"], "comit the current session to the database")

    def run(self, args, ctx):
        ctx.cli.execute(["ls"])
        answer = input(
            "Are you sure you want to comit the session to the database? (Y/n): "
        )
        if answer in ["n", "N"]:
            return
        print("Comitting session to database...")
        ctx.session.commit()
        cli_logger.info("Session comitted to database.")
        return


basic_local_registery = CommandRegistry()
basic_local_registery.register_command(Exit())
basic_local_registery.register_command(Clear())
basic_local_registery.register_command(Entry())
basic_local_registery.register_command(Commit())


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
