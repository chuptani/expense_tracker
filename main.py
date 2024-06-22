import os
import shlex
import readline
import subprocess
import datetime

from commands import Command, CommandRegistry
from utils import error, green, red, is_number, is_date, is_prefix

from basic_commands import basic_local_register


class Cli:

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
        self.weekday_num = self.current_date.weekday()

        self.registry = CommandRegistry()
        self.registry.register_register(basic_local_register)

    def loop(self):

        # intro
        # subprocess.run("clear")
        print("Welcome to Expense Tracker!")
        print()
        print("Use 'help' command to get a list of options")
        print()
        weekday = self.weekdays[self.weekday_num]
        print(f"Today's date: \033[38;5;12m{self.current_date} | {weekday}\033[0m")

        _, columns = os.popen("stty size", "r").read().split()
        print("\033[38;5;237m-\033[0m" * int(columns))

        while True:
            try:

                weekday = self.weekdays[self.weekday_num]
                input_string = shlex.split(
                    input(f"\033[38;5;12m({self.current_date} | {weekday})\033[0m > ")
                )

                _, columns = os.popen("stty size", "r").read().split()

                result = self.registry.execute(input_string)
                if result:
                    print(result, end="")

                print("\033[38;5;237m-\033[0m" * int(columns))

            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                print("\033[38;5;237m-\033[0m" * int(columns))
                continue
            except FileNotFoundError:
                error("category file does not exist")
            except ValueError:
                error("invalid entry:", "quotation not closed")

    def handle_command(self, input_string):
        try:
            if input_string[0].lower() in ["exit", "e"]:
                exit()
            elif input_string[0].lower() in ["clear", "c"]:
                subprocess.run("clear")
            elif input_string[0] in ["date", "d"]:
                input_string.pop(0)
                self.change_date(input_string)
            elif input_string[0] in ["help", "h"]:
                print("lol no")
            elif input_string[0][0] == "+" or is_number(input_string[0]):
                if len(input_string) > 4:
                    error("invalid entry:", "too many arguments")
                elif len(input_string) < 4:
                    error("invalid entry:", "incomplete arguments")
                else:
                    print(self.valid_entry(input_string))
            else:
                error("unknown command:", input_string[0])
        except IndexError:
            pass

    def change_date(self, date_string):
        weekday = self.weekdays[self.weekday_num]
        date_formats = ["%Y-%m-%d", "%m-%d", "%d"]
        new_date = self.today
        # incomplete_date_formats = []
        # date = ""

        if len(date_string) == 0:
            error("no day entered")
            print(f"Current date: {datetime.date.today()}")
            return
        elif len(date_string) > 2:
            error("invalid date:", "too many arguements")
            print(f"Current date: {datetime.date.today()}")
            return
        else:
            date = date_string[0]

        if is_prefix(date, "last"):
            if len(date_string) == 1:
                error("invalid date:", "no weekday provided")
                return
            else:
                date = date_string[1]
            if date in self.dayweeks.keys():
                day = self.dayweeks[date]
                days_since = (self.today.weekday() - day) % 7
                if days_since == 0:
                    days_since = 7
                new_date = self.today - datetime.timedelta(days=days_since)
            else:
                error("invalid date:", f"'{date}' is not a valid weekday")
        elif is_prefix(date, "next"):
            if len(date_string) == 1:
                error("invalid date:", "no weekday provided")
                return
            else:
                date = date_string[1]
            if date in self.dayweeks.keys():
                day = self.dayweeks[date]
                days_till = (day - self.today.weekday()) % 7
                if days_till == 0:
                    days_till = 7
                new_date = self.today + datetime.timedelta(days=days_till)
            else:
                error("invalid date:", f"'{date}' is not a valid weekday")
        elif is_prefix(date, "yesterday"):
            new_date = self.today - datetime.timedelta(days=1)
        elif is_prefix(date, "today"):
            new_date = self.today
        elif is_prefix(date, "tomorrow") or date == "m":
            new_date = self.today + datetime.timedelta(days=1)
        elif is_date(date, date_formats):
            if is_date(date, ["%Y-%m-%d"]):
                new_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            elif is_date(date, ["%m-%d"]):
                new_date = datetime.datetime.strptime(
                    f"{self.today.year}-{date}", "%Y-%m-%d"
                ).date()
            elif is_date(date, ["%d"]):
                new_date = datetime.datetime.strptime(
                    f"{self.today.year}-{self.today.month}-{date}", "%Y-%m-%d"
                ).date()
        else:
            error("unknown date")
            print(f"Current date: {self.current_date} | {weekday}")
            return

        self.current_date = new_date
        self.weekday_num = self.current_date.weekday()
        weekday = self.weekdays[self.weekday_num]
        green(f"Date changed : {new_date} | {weekday}")

    def valid_entry(self, input_string):

        transaction_type = input_string[0][0]
        amount = input_string[0]
        account = input_string[1].lower()
        description = input_string[2]
        category = input_string[3]

        if transaction_type == "+":
            transaction_type = "credit"
            amount = float(amount)
        else:
            transaction_type = "debit"
            amount = float("-" + amount)

        if account in ["cash", "card", "s", "r"]:
            if account == "s":
                account = "cash"
            elif account == "r":
                account = "card"
        else:
            while account not in ["cash", "card", "s", "r"]:
                if account == "":
                    pass
                else:
                    red(f"'{account}' is not a valid account")
                account = input("Is the transaction ca[s]h or ca[r]d? : ").lower()
            if account == "s":
                account = "cash"
            elif account == "r":
                account = "card"
            green(f"Account set to '{account}'")

        with open("categories", "r") as file:
            categories = file.readlines()
        categories = [cat.rstrip("\n") for cat in categories]

        def create_new_category(category):
            if input(f"'{category}' category does not exist. Create it? [Y/n] ") in [
                "y",
                "Y",
                "",
            ]:
                with open("categories", "a") as file:
                    file.write(f"{category}\n")
                green(f"New category created : '{category}'")
                return True
            else:
                return False

        if category in categories:
            pass
        else:
            if create_new_category(category):
                pass
            else:
                while True:
                    category = input("Enter a category: ")
                    if category == "":
                        continue
                    if category in categories:
                        green(f"Category set to '{category}'")
                        break
                    elif create_new_category(category):
                        break

        return [
            self.current_date,
            amount,
            description,
            category,
            account,
            transaction_type,
        ]


if __name__ == "__main__":
    cli = Cli()  # type: ignore
    cli.loop()  # type: ignore
