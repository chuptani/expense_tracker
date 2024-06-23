import datetime


def unique(list):
    return list(set(list))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def valid_num_of_args(args, num, command="", no_args="No args provided"):
    if not args:
        error(command, no_args)
        return False
    elif len(args) > num:
        error(command, "Too many arguments")
        return False
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
