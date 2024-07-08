import datetime


def unique(list):
    return list(set(list))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def valid_num_of_args(args, num, no_args="no args provided"):
    if num > 0 and not args:
        raise ValueError(no_args)
    elif len(args) > num:
        raise ValueError("too many arguments")
    elif len(args) < num:
        raise ValueError("incomplete arguments")
    else:
        return True


def is_date(string, date_formats):
    for date_format in date_formats:
        try:
            datetime.datetime.strptime(string, date_format)
            return True
        except ValueError:
            continue
    return False


def get_date(date, today):
    if is_date(date, ["%Y-%m-%d"]):
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()
    elif is_date(date, ["%m-%d"]):
        return datetime.datetime.strptime(f"{today.year}-{date}", "%Y-%m-%d").date()
    elif is_date(date, ["%d"]):
        return datetime.datetime.strptime(
            f"{today.year}-{today.month}-{date}", "%Y-%m-%d"
        ).date()


def is_prefix(prefix, full_string):
    return full_string.startswith(prefix)


def get_prefixes(s):
    prefixes = []
    for i in range(len(s), 0, -1):
        prefixes.append(s[:i])
    return prefixes


def valid_entry(input_string, ctx):

    global current_date
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

    print([ctx.current_date, amount, description, category, account, transaction_type])


def error(*error_string, new_line=True):
    print("\033[38;5;9mERROR:\033[0m", end=" ")
    for statement in error_string:
        print(statement, end=" ")
    if new_line:
        print()
    else:
        print(end="")


def green(*update_string, new_line=True):
    for statement in update_string:
        print(f"\033[38;5;2m{statement}\033[0m", end=" ")
    if new_line:
        print()
    else:
        print(end="")


def red(*update_string, new_line=True):
    for statement in update_string:
        print(f"\033[38;5;9m{statement}\033[0m", end=" ")
    if new_line:
        print()
    else:
        print(end="")
