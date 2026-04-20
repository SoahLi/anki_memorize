import json

from aqt import gui_hooks, mw

from .processes.init_user_db import init_db_engine
from .processes.update_deck import update_deck


def test():
    if not mw or not mw.col or not mw.col.db:
        print("bruh")
        return

    cards = mw.col.db.all("select * from notes limit 1113")

    for card in cards:
        print(card)

    for model in mw.col.models.all():
        print(json.dumps(model, indent=4))


def test2():
    init_db_engine()
    print("finished")
    update_deck()


def main():
    # gui_hooks.main_window_did_init.append(init_db_engine)
    # gui_hooks.main_window_did_init.append(update_deck)
    gui_hooks.main_window_did_init.append(test2)

    # gui_hooks.main_window_did_init.append(test)


# gui_hooks.main_window_did_init.append(update_playlist_metadata)
