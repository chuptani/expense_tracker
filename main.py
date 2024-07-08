import os
import shlex
import readline
import subprocess
import datetime
import logging


import commands
from commands import CommandRegistry
from utils import utils, validation
from utils.logger import cli_logger, BasicFormatter


class RootFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[0;36m",  # Cyan
        logging.INFO: "\033[0;32m",  # Green
        logging.WARNING: "\033[0;33m",  # Yellow
        logging.ERROR: "\033[0;31m",  # Red
        logging.CRITICAL: "\033[1;31m",  # Bright Red
    }
    RESET = "\033[0m"

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelno)}[%(name)s] - %(levelname)s:{self.RESET} %(message)s"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging.basicConfig(level=logging.DEBUG, handlers=[])
root_logger = logging.getLogger()
file_handler = logging.FileHandler("log")
file_handler.setFormatter(RootFormatter())
root_logger.addHandler(file_handler)

# TODO: create seperate logger to print to stdout

# logger = logging.getLogger(__name__)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(BasicFormatter())
# logger.addHandler(stream_handler)


class cli_CommandRegistry(CommandRegistry):
    def execute(self, args):
        if not args:
            return
        command_name = args[0]
        if command_name == "help":
            return self.help()
        if command_name in self.commands:
            return self.commands[command_name].execute(args[1:], self.ctx)
        try:
            if validation.entry_type(args):
                return self.execute(["add", "entry"] + args)
        except ValueError:
            pass
        cli_logger.error(f"command '{command_name}' not found")


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

        # _, columns = os.popen("stty size", "r").read().split()
        # print("\033[38;5;237m-\033[0m" * int(columns))

        while True:
            try:

                _, columns = os.popen("stty size", "r").read().split()
                print("\033[38;5;237m-\033[0m" * int(columns))

                input_string = shlex.split(
                    input(
                        f"\033[38;5;12m({self.ctx.current_date} | {self.ctx.weekday})\033[0m > "
                    )
                )

                self.registry.execute(input_string)

            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                # print("\033[38;5;237m-\033[0m" * int(columns))
                continue
            except FileNotFoundError:
                utils.error("category file does not exist")
            except ValueError as e:
                pass
                # logger.error(e)


if __name__ == "__main__":
    Cli().loop()
