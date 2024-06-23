class Command:
    def __init__(
        self,
        names,
        help_text="",
    ):
        self.name = names.pop(0)
        self.aliases = names
        self.help_text = help_text
        self.subcommands = {}

    def add_subcommand(self, subcommand):
        self.subcommands[subcommand.name] = subcommand
        for alias in subcommand.aliases:
            self.subcommands[alias] = subcommand

    def execute(self, args, ctx):
        if args and args[0] == "help":
            print(self.help(), end="")
        elif args and args[0] in self.subcommands:
            subcommand = self.subcommands[args[0]]
            subcommand.execute(args[1:], ctx)
        else:
            self.run(args, ctx)

    def run(self, args, ctx):
        raise NotImplementedError(f"Command {self.name} not implemented.")

    def help(self):
        help_message = f"{self.name}: {self.help_text}\n"
        for subcommand in list(set(self.subcommands.values())):
            help_message += f"  {subcommand.name}: {subcommand.help_text}\n"
        return help_message


class CommandRegistry:
    def __init__(self, ctx=None):
        self.commands = {}
        self.ctx = ctx

    def register_command(self, command):
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command

    def register_registery(self, register):
        for command in list(set(register.commands.values())):
            self.commands[command.name] = command
            for alias in command.aliases:
                self.commands[alias] = command

    def execute(self, args):
        # args = command_line.split()
        if not args:
            return print("No command provided.")
        elif args[0] == "help":
            return self.help()
        command_name = args.pop(0)
        if command_name in self.commands:
            return self.commands[command_name].execute(args, self.ctx)
        print(f"Unknown command: {command_name}")

    def help(self):
        help_message = "Available commands:\n\n"
        for command in list(set(self.commands.values())):
            help_message += command.help() + "\n"
        print(help_message, end="")
