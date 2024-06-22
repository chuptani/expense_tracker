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
        for subcommand in list(set(self.subcommands.values())):
            help_message += f"  {subcommand.name}: {subcommand.help_text}\n"
        return help_message


class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register_command(self, command):
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command

    def register_register(self, register):
        for command in list(set(register.commands.values())):
            self.commands[command.name] = command
            for alias in command.aliases:
                self.commands[alias] = command

    def execute(self, args):
        # args = command_line.split()
        if not args:
            return "No command provided."
        elif args[0] == "help":
            return self.help()
        command_name = args.pop(0)
        if command_name in self.commands:
            return self.commands[command_name].execute(args)
        return f"Unknown command: {command_name}"

    def help(self):
        help_message = "Available commands:\n"
        for command in list(set(self.commands.values())):
            help_message += command.help()
        return help_message
