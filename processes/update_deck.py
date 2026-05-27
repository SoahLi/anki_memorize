import time
from aqt import QTimer
from aqt.operations import QueryOp
from aqt.utils import showInfo, tooltip
from processes.DatabaseManager import DatabaseManager
from custom_types.Note import Note
from util.anki_getters import get_mw
from util.config import config_get
from util.getters import get_platform_handler_by_name
from util.ui.status_timer import StatusBarTimer


def update_deck():
    potential_platforms: list[str] = config_get("platforms") or []
    platforms: list[str] = []

    for platform_name in potential_platforms:
        if platform_name is None:
            print(f"Platform {platform_name} not found, skipping.")
            continue
        platforms.append(platform_name)

    if not platforms:
          get_mw().statusBar().showMessage("No platforms configured.", 3000) #pyright: ignore[reportOptionalMemberAccess]
          return
    notes: list[Note] = []
    remaining = len(platforms)
    print( f"Updating deck with platforms: {platforms}. Remaining: {remaining}")

    #processed in the main thread (at least that's what claude says)
    def on_success(result: list[Note]):
        nonlocal remaining
        notes.extend(result)

        remaining -= 1
        if remaining == 0:
            # TODO: perform bulk, atomic update
            DatabaseManager.add_notes(notes)
            StatusBarTimer.stop_timer()
            get_mw().statusBar().showMessage(f"Finished updating SM_memorize with {len(notes)} notes", 3000) # pyright: ignore[reportOptionalMemberAccess] 




    StatusBarTimer.start_timer()
    for platform_name in platforms:
        platform = get_platform_handler_by_name(platform_name)
        op = QueryOp(
            # the active window (main window in this case)
            parent=get_mw(),
            # the operation is passed the collection for convenience; you can
            # ignore it if you wish
            op=lambda col, p=platform: p.update(), # pyright: ignore[reportOptionalMemberAccess]
            # this function will be called if op completes successfully,
            # and it is given the return value of the op
            success= on_success 
        )


        # if with_progress() is not called, no progress window will be shown.
        # note: QueryOp.with_progress() was broken until Anki 2.1.50
        op.run_in_background()

