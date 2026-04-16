import json

from aqt import gui_hooks, mw

from .processes.update_playlist_metadata import update_playlist_metadata


def test():
    if not mw or not mw.col or not mw.col.db:
        print("bruh")
        return

    cards = mw.col.db.all("select * from notes limit 1113")

    for card in cards:
        print(card)

    for model in mw.col.models.all():
        print(json.dumps(model, indent=4))


def main():
    # gui_hooks.main_window_did_init.append(test)
    gui_hooks.main_window_did_init.append(update_playlist_metadata)
