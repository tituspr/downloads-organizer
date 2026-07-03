from logger import logger
import os
import shutil

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")


def get_unique_filepath(destination_folder, filename):
    """
    Returns a file path that doesn't already exist.
    Example:
        Report.pdf
        Report (1).pdf
        Report (2).pdf
    """

    name, extension = os.path.splitext(filename)

    candidate = os.path.join(destination_folder, filename)

    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(
            destination_folder,
            f"{name} ({counter}){extension}"
        )
        counter += 1

    return candidate


def move_file(filepath, destination):

    destination_folder = os.path.join(DOWNLOADS_FOLDER, destination)

    os.makedirs(destination_folder, exist_ok=True)

    filename = os.path.basename(filepath)

    new_path = get_unique_filepath(destination_folder, filename)

    new_filename = os.path.basename(new_path)

    if new_filename != filename:
        logger.info(
            f"Duplicate detected: '{filename}' -> '{new_filename}'"
        )

    shutil.move(filepath, new_path)

    logger.info(f"Moved to: {new_path}")