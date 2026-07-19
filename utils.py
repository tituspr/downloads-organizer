import time

from config import (
    TEMP_FILE_EXTENSIONS,
    TEMP_FILE_PREFIXES,
    DUPLICATE_EVENT_WINDOW
)

from config import (
    FILE_READY_TIMEOUT,
    FILE_READY_RETRY_DELAY,
)

processed_files = {}


def is_temporary_file(filename, filepath):
    return (
        filename.startswith(TEMP_FILE_PREFIXES)
        or filepath.endswith(TEMP_FILE_EXTENSIONS)
    )


def is_recently_processed(filepath: str) -> bool:
    current_time = time.time()

    # Remove expired entries
    expired_files = [
        path
        for path, timestamp in processed_files.items()
        if current_time - timestamp > DUPLICATE_EVENT_WINDOW
    ]

    for path in expired_files:
        del processed_files[path]

    # Check if this file was processed recently
    if filepath in processed_files:
        return True

    # Record this file
    processed_files[filepath] = current_time
    return False


def wait_for_file_ready(filepath: str, timeout: int = FILE_READY_TIMEOUT) -> bool:
    """
    Wait until a file becomes readable before processing.
    Returns True if ready, otherwise False.
    """

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            with open(filepath, "rb"):
                return True
        except PermissionError:
            time.sleep(FILE_READY_RETRY_DELAY)
        except FileNotFoundError:
            return False

    return False