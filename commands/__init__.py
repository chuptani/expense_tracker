from .commands import Command, CommandRegistry

from .basic_commands import basic_local_registery
from .date_commands import date_local_registery
from .add_commands import add_local_registery
from .list_commands import list_local_registery
from .get_commands import get_local_registry
from .delete_commands import delete_local_registry

package_registry = CommandRegistry()
package_registry.register_registery(basic_local_registery)
package_registry.register_registery(date_local_registery)
package_registry.register_registery(add_local_registery)
package_registry.register_registery(list_local_registery)
package_registry.register_registery(get_local_registry)
package_registry.register_registery(delete_local_registry)
