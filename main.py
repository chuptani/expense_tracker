import os
import readline
import subprocess
import datetime


weekdays = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun",
}

dayweeks = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}

now = datetime.datetime.now()
today = now.date()
current_date = today
weekday_num = current_date.weekday()


def main():
    global current_daate, weekday_num

    # subprocess.run("clear")
    print("Welcome to Expense Tracker!")
    print()
    print("Use 'help' command to get a list of options")
    print()
    weekday = weekdays[weekday_num]
    print(f"Today's date: \033[38;5;12m{current_date} | {weekday}\033[0m")

    _, columns = os.popen("stty size", "r").read().split()
    print("\033[38;5;237m-\033[0m" * int(columns))

    while True:
        try:

            weekday = weekdays[weekday_num]
            input_string = input(
                f"\033[38;5;12m({current_date} | {weekday})\033[0m > "
            ).split()

            _, columns = os.popen("stty size", "r").read().split()

            if input_string[0].lower() == "exit":
                exit()
            elif input_string[0].lower() == "clear":
                subprocess.run("clear")
            else:
                handle_command(input_string)

            print("\033[38;5;237m-\033[0m" * int(columns))

        except EOFError:
            break
        except KeyboardInterrupt:
            break


def handle_command(input_string):
    if input_string[0] == "date":
        input_string.pop(0)
        change_date(input_string)
    elif input_string[0] == "help":
        print("No")
    elif input_string[0][0] == "+" or input_string[0][0] == "-":
        print("test")

    else:
        error("unknown command:", input_string[0])


def change_date(date_string):
    global today, current_date, dayweeks, weekday_num

    if len(date_string) == 0:
        error("no day entered")
        print(f"Current date: {datetime.date.today()}")
        return
    else:
        if date_string[0] == "yesterday":
            new_date = today - datetime.timedelta(days=1)
        elif date_string[0] == "today":
            new_date = today
        elif date_string[0] == "tomorrow":
            new_date = today + datetime.timedelta(days=1)
        elif date_string[0] in dayweeks.keys():
            day = dayweeks[date_string[0]]
            days_since = (today.weekday() - day) % 7
            if days_since == 0:
                days_since = 7
            new_date = today - datetime.timedelta(days=days_since)
        else:
            error("unknown date")
            weekday = weekdays[weekday_num]
            print(f"Current date: {current_date} | {weekday}")
            return

    current_date = new_date
    weekday_num = current_date.weekday()
    weekday = weekdays[weekday_num]
    print(f"Date changed : {new_date} | {weekday}")


def error(*error_string):
    print("\033[38;5;160mERROR:\033[0m", end=" ")
    for statement in error_string:
        print(statement, end=" ")
    print()


if __name__ == "__main__":
    main()
