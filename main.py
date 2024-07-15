import os
import shlex
import logging
import readline
import datetime

from context import Ctx
import commands
from utils import validation
from utils.logger import red
from database.models import session
from sqlalchemy.exc import SQLAlchemyError


class RootFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[0;36m",  # Cyan
        logging.INFO: "\033[0;32m",  # Green
        logging.WARNING: "\033[0;33m",  # Yellow
        logging.ERROR: "\033[0;31m",  # Red
        logging.CRITICAL: "\033[1;31m",  # Red1
    }
    RESET = "\033[0m"

    def format(self, record):
        # log_fmt = f"{self.COLORS.get(record.levelno)}[%(name)s] - %(levelname)s:{self.RESET} %(message)s"
        log_fmt = f"{self.COLORS.get(record.levelno)}[%(asctime)s] - [%(name)s] - %(levelname)s:{self.RESET} %(message)s"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# log_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
# log_path = f"logs/{log_name}.log"
logging.basicConfig(level=logging.DEBUG, handlers=[])
root_logger = logging.getLogger()
file_handler = logging.FileHandler("logs/cli.log")
file_handler.setFormatter(RootFormatter())
root_logger.addHandler(file_handler)


class cli_CommandRegistry(commands.CommandRegistry):
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
            red(f"command '{command_name}' not found")


class Cli:

    def __init__(self):

        self.ctx = Ctx(session)
        self.registry = cli_CommandRegistry(self.ctx)
        self.registry.register_registery(commands.package_registry)

        self.ctx.cli = self.registry

    def loop(self):

        # intro
        # subprocess.run("clear")
        print("Welcome to Expense Tracker!")
        print()
        print("Use 'help' command to get a list of options")
        print()
        print(
            f"Today's date: \033[38;5;12m{self.ctx.current_date} | {self.ctx.current_week.weekday}\033[0m"
        )
        root_logger.info("CLI started")

        while True:
            try:

                _, columns = os.popen("stty size", "r").read().split()
                print("\033[38;5;237m-\033[0m" * int(columns))

                input_string = shlex.split(
                    input(
                        f"\033[38;5;12m({self.ctx.current_date} | {self.ctx.current_week.weekday})\033[0m > "
                    )
                )

                self.registry.execute(input_string)

            except EOFError:
                break
            except KeyboardInterrupt:
                print()
            except ValueError as e:
                root_logger.error(e)
                red(e)
            except NotImplementedError as e:
                root_logger.error(e)
                red(e)
            except SQLAlchemyError as e:
                session.rollback()
                root_logger.error(e)
                red(e)


if __name__ == "__main__":
    Cli().loop()
