import os
import shlex
import readline
import subprocess
import datetime

import commands
from commands.commands import CommandRegistry
import utils


class cli_CommandRegistry(CommandRegistry):
    def execute(self, args):
        if not args:
            return print("No command provided.")
        command_name = args[0]
        if command_name == "help":
            return self.help()
        if command_name in self.commands:
            return self.commands[command_name].execute(args[1:], self.ctx)
        if command_name[0] == "+" or utils.is_number(command_name):
            return self.commands["entry"].execute(args, self.ctx)
        utils.error(f"Command '{command_name}' not found")
        print()
        return self.help()


class ctx:
    def __init__(self):
        self.weekdays = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        }

        self.dayweeks = {
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6,
        }

        self.now = datetime.datetime.now()
        self.today = self.now.date()
        self.current_date = self.today
        self.weekday_num = self.today.weekday()
        self.weekday = self.weekdays[self.weekday_num]

        self.date_formats = ["%Y-%m-%d", "%m-%d", "%d"]

    def new_date(self, date=datetime.datetime.now().date()):
        self.current_date = date
        self.weekday_num = date.weekday()
        self.weekday = self.weekdays[self.weekday_num]


class Cli:

    def __init__(self):
        self.ctx = ctx()

        self.registry = cli_CommandRegistry(self.ctx)
        self.registry.register_registery(commands.package_registry)

    def loop(self):

        # intro
        # subprocess.run("clear")
        print("Welcome to Expense Tracker!")
        print()
        print("Use 'help' command to get a list of options")
        print()
        self.ctx.weekday = self.ctx.weekdays[self.ctx.weekday_num]
        print(
            f"Today's date: \033[38;5;12m{self.ctx.current_date} | {self.ctx.weekday}\033[0m"
        )

        _, columns = os.popen("stty size", "r").read().split()
        print("\033[38;5;237m-\033[0m" * int(columns))

        while True:
            try:

                input_string = shlex.split(
                    input(
                        f"\033[38;5;12m({self.ctx.current_date} | {self.ctx.weekday})\033[0m > "
                    )
                )

                _, columns = os.popen("stty size", "r").read().split()

                self.registry.execute(input_string)

                print("\033[38;5;237m-\033[0m" * int(columns))

            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                print("\033[38;5;237m-\033[0m" * int(columns))
                continue
            except FileNotFoundError:
                utils.error("category file does not exist")
            except ValueError:
                utils.error("invalid entry:", "quotation not closed")


if __name__ == "__main__":
    cli = Cli()  # type: ignore
    cli.loop()  # type: ignore
