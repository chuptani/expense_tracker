import datetime


def unique(list):
    return list(set(list))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_date(string, date_formats):
    for date_format in date_formats:
        try:
            datetime.datetime.strptime(string, date_format)
            return True
        except ValueError:
            continue
    return False


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
