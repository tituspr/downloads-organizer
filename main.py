import os
import threading
from pathlib import Path
import pystray
from PIL import Image
from watcher import DownloadWatcher
import time

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


def main():

    watcher_thread.start()

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
            pystray.MenuItem("Open Logs", open_logs),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", on_exit),
        ),
    )

    icon.run()


if __name__ == "__main__":
    main()