from commands.commands import Command, CommandRegistry

from commands.basic_commands import basic_local_registery

# from date_commands import date_local_registery

package_registry = CommandRegistry()

package_registry.register_registery(basic_local_registery)
