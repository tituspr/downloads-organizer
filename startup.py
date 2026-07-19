import os
import sys
from pathlib import Path
from win32com.client import Dispatch

APP_NAME = "Downloads Organizer"

SHORTCUT_DESCRIPTION = (
    "Automatically starts Downloads Organizer when you sign in."
)


def get_startup_folder():
    return Path(
        os.environ["APPDATA"],
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )


def get_shortcut_path():
    return get_startup_folder() / f"{APP_NAME}.lnk"


def get_target():
    """
    Returns:
        target      -> executable
        arguments   -> command line arguments
        working_dir -> working directory
    """
    if getattr(sys, "frozen", False):
        return (
            sys.executable,
            "",
            Path(sys.executable).parent,
        )

    main_file = Path(__file__).parent / "main.py"

    return (
        sys.executable,
        f'"{main_file}"',
        Path(__file__).parent,
    )


def enable_startup():
    shortcut = Dispatch("WScript.Shell").CreateShortCut(
        str(get_shortcut_path())
    )

    target, arguments, working_dir = get_target()

    shortcut.TargetPath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = str(working_dir)
    shortcut.IconLocation = target
    shortcut.Description = SHORTCUT_DESCRIPTION

    shortcut.save()


def disable_startup():
    shortcut = get_shortcut_path()

    if shortcut.exists():
        shortcut.unlink()


def is_startup_enabled():
    return get_shortcut_path().exists()