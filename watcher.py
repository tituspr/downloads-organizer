from organizer import move_file
from logger import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import time
import os

from requests.exceptions import (
    ConnectionError,
    Timeout,
    RequestException
)

from utils import (
    is_temporary_file,
    is_recently_processed,
    wait_for_file_ready
)

from config import (
    WEBHOOK_URL,
    DOWNLOADS_FOLDER,
    TEMP_FILE_EXTENSIONS,
    TEMP_FILE_PREFIXES
)

from utils import is_recently_processed

class DownloadHandler(FileSystemEventHandler):

    def process_file(self, filepath):

        filename = os.path.basename(filepath)

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

        filename = os.path.basename(filepath)
        extension = os.path.splitext(filename)[1].lower()

        payload = {
            "name": filename,
            "extension": extension,
            "path": filepath
        }

        logger.info(f"Detected: {filename}")

        try:
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            destination = data.get("destination")

            if not destination:
                raise KeyError("destination")

            logger.info(
                f"Webhook response: {response.status_code} ({destination})"
                        )

            move_file(filepath, destination)

        except ConnectionError:
            logger.error("Could not connect to n8n. Is the workflow running?")

        except Timeout:
            logger.error("Request to n8n timed out.")

        except KeyError:
            logger.error("Webhook response missing 'destination'.")

        except ValueError:
            logger.error("Invalid JSON returned from webhook.")

        except PermissionError:
            logger.error("Permission denied while moving file.")

        except FileNotFoundError:
            logger.error("Source file no longer exists.")

        except RequestException as e:
            logger.error(f"HTTP request failed: {e}")

        except Exception:
            logger.exception("Unexpected error occurred.")

    def on_created(self, event):
        if event.is_directory:
            return

        self.process_file(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        
        logger.info(f"Moved event: {os.path.basename(event.dest_path)}")
        self.process_file(event.dest_path)

observer = Observer()
observer.schedule(
    DownloadHandler(),
    DOWNLOADS_FOLDER,
    recursive=False
)

observer.start()

logger.info(f"Watching: {DOWNLOADS_FOLDER}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()