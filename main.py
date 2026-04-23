from aqt import gui_hooks

from .processes.init_user_db import init_db_engine
from .processes.update_deck import update_deck


# I would like to call these with two seperate main_window_did_init calls
def starting_processes():
    init_db_engine()
    update_deck()


def main():
    gui_hooks.main_window_did_init.append(starting_processes)
