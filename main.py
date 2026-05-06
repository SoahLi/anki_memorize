from aqt import gui_hooks

from .processes.DatabaseManager import DatabaseManager
from .processes.update_deck import update_deck
from .util.platform_registry import init_platform_registry


# I would like to call these with two seperate main_window_did_init calls
def starting_processes():
    DatabaseManager.create()
    init_platform_registry(DatabaseManager.get_platform_id_by_name("youtube"))
    update_deck()


def main():
    gui_hooks.main_window_did_init.append(starting_processes)
