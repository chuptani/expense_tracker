import sys, subprocess
from commands.commands import Command, CommandRegistry
import utils


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


basic_local_registery = CommandRegistry()
basic_local_registery.register_command(Exit())
basic_local_registery.register_command(Clear())


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
