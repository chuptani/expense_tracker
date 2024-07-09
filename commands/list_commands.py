import logging
from commands import Command, CommandRegistry
from utils.logger import BasicFormatter


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(BasicFormatter())
logger.addHandler(handler)


class List(Command):
    def __init__(self):
        super().__init__(["list", "ls"], "list all entries")

    def run(self, args, ctx):
        if all(not value for value in ctx.session_additions.values()):
            print("List of additions:")
            for key in ctx.session_additions:
                if ctx.session_additions[key]:
                    print(f"\n{key.capitalize()}:")
                    for item in ctx.session_additions[key]:
                        print(item)
        if all(not value for value in ctx.session_deletions.values()):
            print("\nList of deletions:")
            for key in ctx.session_deletions:
                if ctx.session_deletions[key]:
                    print(f"\n{key.capitalize()}:")
                    for item in ctx.session_deletions[key]:
                        print(item)
        if all(not value for value in ctx.session_updates.values()):
            print("\nList of updates:")
            for key in ctx.session_updates:
                if ctx.session_updates[key]:
                    print(f"\n{key.capitalize()}:")
                    for item in ctx.session_updates[key]:
                        print(item)
        print()


ls = List()

list_local_registery = CommandRegistry()
list_local_registery.register_command(ls)


def main():
    registry = CommandRegistry()

    while True:
        try:
            command_line = input("> ")
            registry.execute(command_line)
        except SystemExit:
            exit()


if __name__ == "__main__":
    main()
