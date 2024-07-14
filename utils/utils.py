import datetime


def unique(list):
    return list(set(list))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def if_args_get_arg(args, expected_args):
    if len(args) > expected_args:
        return args[expected_args]
    return None


def valid_num_of_args(
    args,
    num,
    no_args="no arguments provided",
    extra_args="too many arguments",
    incomplete_args="incomplete arguments",
):
    if num > 0 and not args:
        raise ValueError(no_args)
    elif len(args) > num:
        raise ValueError(extra_args)
    elif len(args) < num:
        raise ValueError(incomplete_args)
    else:
        return True


def is_date(string, date_formats):
    for date_format in date_formats:
        try:
            datetime.datetime.strptime(string, date_format)
            return True
        except ValueError:
            pass
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
    raise ValueError(f"date format not recognized: '{date}'")


def is_prefix(prefix, full_string):
    return full_string.startswith(prefix)


def get_prefixes(s):
    prefixes = []
    for i in range(len(s), 0, -1):
        prefixes.append(s[:i])
    return prefixes


if __name__ == "__main__":
    for alias in get_prefixes("hello"):
        print(alias)
