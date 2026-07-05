import os
import threading
from pathlib import Path
import pystray
from PIL import Image
from watcher import DownloadWatcher
import startup
import settings

watcher = DownloadWatcher()

watcher_thread = threading.Thread(
    target=watcher.start,
    daemon=True
)


def create_icon():

    icon_path = Path(__file__).parent / "assets" / "icon.ico"
    return Image.open(icon_path)


def open_logs(icon, item):
    log_path = Path(__file__).parent / "logs" / "organizer.log"
    os.startfile(log_path)


def on_exit(icon, item):
    watcher.stop()
    watcher_thread.join(timeout=3)
    icon.stop()


def on_toggle_pause(icon, item):

    watcher.toggle_pause()

    icon.update_menu()


def on_toggle_startup(icon, item):

    if startup.is_startup_enabled():
        startup.disable_startup()
    else:
        startup.enable_startup()

    icon.update_menu()


def main():


    watcher_thread.start()

    def open_settings(icon, item):
        settings.show()


    icon = pystray.Icon(
        "Downloads Organizer v1.3",
        create_icon(),
        "Downloads Organizer v1.3",
    menu=pystray.Menu(

        pystray.MenuItem(
            lambda item: watcher.pause_menu_text,
            on_toggle_pause,
        ),

        pystray.Menu.SEPARATOR,

        pystray.MenuItem(
            "Start with Windows",
            on_toggle_startup,
            checked=lambda item: startup.is_startup_enabled(),
        ),

        pystray.Menu.SEPARATOR,

        pystray.MenuItem(
            "Settings...",
            open_settings,
        ),

        pystray.Menu.SEPARATOR,

        pystray.MenuItem("Open Logs", open_logs),

        pystray.Menu.SEPARATOR,

        pystray.MenuItem("Exit", on_exit),
    ),
    )

    icon.run()

if __name__ == "__main__":
    main()