from commands import Command, CommandRegistry
import datetime
import utils


def date_changed(ctx):
    utils.green(f"Date changed : {ctx.current_date} | {ctx.weekday}")


def date_not_changed(ctx):
    print(f"Current date : {ctx.current_date} | {ctx.weekday}")


class Date(Command):
    def __init__(self):
        super().__init__(["date", "d"], "change current date")

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 1):
            date_not_changed(ctx)
            return

        if utils.is_date(args[0], ctx.date_formats):
            ctx.new_date(utils.get_date(args[0], ctx.today))
            date_changed(ctx)
        else:
            utils.error("invalid date")
            date_not_changed(ctx)


class Last(Command):
    def __init__(self):
        super().__init__(["last", "l"], "change to last weekday")

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
            utils.error("invalid date:", f"'{args[0]}' is not a valid weekday")


class Next(Command):
    def __init__(self):
        super().__init__(["next", "n"], "change to next weekday")

    def run(self, args, ctx):
        if not utils.valid_num_of_args(args, 1, "invalid date:", "no weekday provided"):
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
            utils.error("invalid date:", f"'{args[0]}' is not a valid weekday")


date = Date()
date.add_subcommand(Last())
date.add_subcommand(Next())

date_local_registery = CommandRegistry()
date_local_registery.register_command(date)
