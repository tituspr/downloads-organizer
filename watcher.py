import os
import time
from enum import Enum, auto

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from logger import logger
from organizer import move_file
from utils import (
    is_temporary_file,
    is_recently_processed,
    wait_for_file_ready
)
from webhook import classify_file

from config import (
    DOWNLOADS_FOLDER,
    get_config,
)


class WatcherState(Enum):
    RUNNING = auto()
    PAUSED = auto()
    STOPPING = auto()


class DownloadHandler(FileSystemEventHandler):

    def __init__(self, watcher):
        super().__init__()
        self.watcher = watcher

    def process_file(self, filepath):

        filename = os.path.basename(filepath)

        if self.watcher.is_paused:
            logger.info(f"Ignored while paused: {filename}")
            return

        # Ignore temporary files
        if is_temporary_file(filename, filepath):
            logger.info(f"Ignored temporary file: {filename}")
            return

        # Ignore duplicate events
        if is_recently_processed(filepath):
            logger.info(f"Skipped duplicate event: {filename}")
            return

        # Wait for the file to finish copying/downloading
        if not wait_for_file_ready(filepath):
            logger.warning(f"File not ready: {filename}")
            return

        delay = get_config("organize_delay")

        if delay > 0:
            logger.info(
                f"Waiting {delay} seconds before organizing '{filename}'"
            )
            time.sleep(delay)

        extension = os.path.splitext(filename)[1].lower()

        payload = {
            "name": filename,
            "extension": extension,
            "path": filepath
        }

        logger.info(f"Detected: {filename}")

        destination = classify_file(payload)

        if destination:
            move_file(filepath, destination)

    def on_created(self, event):
        if event.is_directory:
            return

        self.process_file(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        
        logger.info(f"Moved event: {os.path.basename(event.dest_path)}")
        self.process_file(event.dest_path)


class DownloadWatcher:

    def __init__(self):
        self.observer = Observer()
        self.state = WatcherState.RUNNING

    @property
    def is_running(self):
        return self.state == WatcherState.RUNNING

    @property
    def is_paused(self):
        return self.state == WatcherState.PAUSED

    @property
    def pause_menu_text(self):
        return (
            "▶ Resume Watching"
            if self.is_paused
            else "⏸ Pause Watching"
        )

    def start(self):

        self.state = WatcherState.RUNNING

        self.observer.schedule(
            DownloadHandler(self),
            DOWNLOADS_FOLDER,
            recursive=False
        )

        self.observer.start()

        logger.info(f"Watching: {DOWNLOADS_FOLDER}")

        try:
            while self.observer.is_alive():
                time.sleep(1)
        finally:
            self.observer.join()


    def stop(self):

        if self.state == WatcherState.STOPPING:
            return

        self.state = WatcherState.STOPPING

        logger.info("Stopping watcher...")

        self.observer.stop()


    def pause(self):

        if self.state == WatcherState.RUNNING:
            self.state = WatcherState.PAUSED
            logger.info("Watcher paused")


    def resume(self):

        if self.state == WatcherState.PAUSED:
            self.state = WatcherState.RUNNING
            logger.info("Watcher resumed")


    def toggle_pause(self):
        if self.is_paused:
            self.resume()
        else:
            self.pause()


    def join(self):
        self.observer.join()