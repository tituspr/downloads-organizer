import threading
import watcher
from pathlib import Path

import pystray
from PIL import Image


def create_icon():
    icon_path = Path(__file__).parent / "assets" / "icon.ico"
    return Image.open(icon_path)


def on_exit(icon, item):
    icon.stop()

def start_watcher():
    watcher.main()

def main():
    icon = pystray.Icon(
        "downloads_organizer",
        create_icon(),
        "Downloads Organizer",
        menu=pystray.Menu(
            pystray.MenuItem("Exit", on_exit)
        ),
    )

    icon.run()


if __name__ == "__main__":
    main()