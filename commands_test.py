import commands


class GreetCommand(commands.Command):
    def __init__(self):
        super().__init__("greet", "Greet the user")

    def run(self, args):
        if args:
            return f"Hello, {' '.join(args)}!"
        return "Hello!"


class ExitCommand(commands.Command):
    def __init__(self):
        super().__init__("exit", "Exit the program")

    def run(self, args):
        return "Exiting the program..."


def main():
    registry = commands.CommandRegistry()

    # Register commands
    greet_command = GreetCommand()
    greet_command.add_subcommand(GreetCommand())  # Adding subcommand for demonstration
    registry.register(greet_command)
    registry.register(ExitCommand())

    # Command loop
    while True:
        command_line = input("> ")
        result = registry.execute(command_line)
        print(result)
        if result == "Exiting the program...":
            break


if __name__ == "__main__":
    main()
