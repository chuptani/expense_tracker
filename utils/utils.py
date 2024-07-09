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
