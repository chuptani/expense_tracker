import logging
from commands import Command, CommandRegistry
import datetime
from utils import utils
from utils.logger import BasicFormatter, cli_logger


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


def date_changed(ctx):
    cli_logger.info(f"Date changed : {ctx.current_date} | {ctx.current_week.weekday}")


def date_not_changed(ctx):
    print(f"Current date : {ctx.current_date} | {ctx.current_week.weekday}")


class Date(Command):
    def __init__(self):
        super().__init__(
            ["date", "d"],
            "change current date\nallowed formats: yyyy-mm-dd, mm-dd, dd",
        )

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 1):
            date_not_changed(ctx)
            return

        if utils.is_date(args[0], ctx.date_formats):
            ctx.new_date(utils.get_date(args[0], ctx.today))
            date_changed(ctx)
        else:
            cli_logger.info("invalid date")
            date_not_changed(ctx)


class Yesterday(Command):
    def __init__(self):
        super().__init__(["yesterday", "yes"], "change to yesterday")

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 0, "date:"):
            date_not_changed(ctx)
            return
        ctx.new_date(ctx.today - datetime.timedelta(days=1))
        date_changed(ctx)


class Tomorrow(Command):
    def __init__(self):
        super().__init__(["tomorrow", "tom"], "change to tomorrow")

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 0, "date:"):
            date_not_changed(ctx)
            return
        ctx.new_date(ctx.today + datetime.timedelta(days=1))
        date_changed(ctx)


class Today(Command):
    def __init__(self):
        super().__init__(["today", "tod"], "change to tomorrow")

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 0, "date:"):
            date_not_changed(ctx)
            return
        ctx.new_date(ctx.today)
        date_changed(ctx)


class Last(Command):
    def __init__(self):
        super().__init__(
            ["last", "l"], "change to last weekday (e.g. args: mon, tue, etc.)"
        )

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 1, "no weekday provided"):
            date_not_changed(ctx)
            return
        if args[0] in ctx.dayweeks.keys():
            day = ctx.dayweeks[args[0]]
            days_since = (ctx.today.weekday() - day) % 7
            if days_since == 0:
                days_since = 7
            ctx.new_date(ctx.today - datetime.timedelta(days=days_since))
            date_changed(ctx)
        else:
            logger.error("invalid date:", f"'{args[0]}' is not a valid weekday")


class Next(Command):
    def __init__(self):
        super().__init__(
            ["next", "n"], "change to next weekday (e.g. args: mon, tue, etc.)"
        )

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 1, "no weekday provided"):
            date_not_changed(ctx)
            return
        if args[0] in ctx.dayweeks.keys():
            day = ctx.dayweeks[args[0]]
            days_till = (day - ctx.today.weekday()) % 7
            if days_till == 0:
                days_till = 7
            ctx.new_date(ctx.today + datetime.timedelta(days=days_till))
            date_changed(ctx)
        else:
            logger.error("invalid date:", f"'{args[0]}' is not a valid weekday")


date = Date()
date.add_subcommand(Last())
date.add_subcommand(Next())
date.add_subcommand(Yesterday())
date.add_subcommand(Tomorrow())
date.add_subcommand(Today())

date_local_registery = CommandRegistry()
date_local_registery.register_command(date)


def main():
    registry = CommandRegistry()

    registry.register_command(date)

    while True:
        try:
            command_line = input("> ")
            result = registry.execute(command_line)
            if result:
                print(result)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
