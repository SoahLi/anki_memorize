
# --- Animated status bar timer ---
from aqt import QTimer
from util.anki_getters import get_mw


class StatusBarTimer:
    timer = None

    @classmethod
    def start_timer(cls):
        mw = get_mw()
        dot_state = [1]  # 1, 2, or 3 dots; mutable so the closure can modify it
        cls.timer = QTimer(mw)
        cls.timer.setInterval(500)
        def tick():
            dots = "." * dot_state[0]
            mw.statusBar().showMessage(f"Updating SM_memorize{dots}")  # pyright: ignore[reportOptionalMemberAccess]
            dot_state[0] = (dot_state[0] % 3) + 1  # cycles 1 → 2 → 3 → 1

        cls.timer.timeout.connect(tick)
        tick()        # show immediately before the first 500 ms elapses
        cls.timer.start()

    @classmethod
    def stop_timer(cls):
        if cls.timer is not None:
            cls.timer.stop()

