import sys, subprocess
from commands import Command, CommandRegistry
from utils import utils


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


basic_local_registery = CommandRegistry()
basic_local_registery.register_command(Exit())
basic_local_registery.register_command(Clear())
basic_local_registery.register_command(Entry())


def main():
    registry = CommandRegistry()

    registry.register_command(Exit())
    registry.register_command(Clear())

    while True:
        try:
            command_line = input("> ")
            result = registry.execute(command_line)
            if result:
                print(result)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
