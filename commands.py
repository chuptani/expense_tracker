class Command:
    def __init__(self, name, help_text=""):
        self.name = name
        self.help_text = help_text
        self.subcommands = {}

    def add_subcommand(self, subcommand):
        self.subcommands[subcommand.name] = subcommand

    def execute(self, args):
        if args and args[0] == "help":
            print(self.help())
        elif args and args[0] in self.subcommands:
            subcommand = self.subcommands[args[0]]
            return subcommand.execute(args[1:])
        else:
            return self.run(args)

    def run(self, args):
        raise NotImplementedError(f"Command {self.name} not implemented.")

    def help(self):
        help_message = f"{self.name}: {self.help_text}\n"
        for subcommand in self.subcommands.values():
            help_message += f"  {subcommand.name}: {subcommand.help_text}\n"
        return help_message


class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, command):
        self.commands[command.name] = command

    def execute(self, command_line):
        args = command_line.split()
        if not args:
            return "No command provided."
        command_name = args.pop(0)
        if command_name in self.commands:
            return self.commands[command_name].execute(args)
        return f"Unknown command: {command_name}"

    def help(self):
        help_message = "Available commands:\n"
        for command in self.commands.values():
            help_message += command.help()
        return help_message
