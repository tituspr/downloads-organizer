import os

# Webhook
WEBHOOK_URL = "http://localhost:5678/webhook/downloads-organizer"

# Downloads folder
DOWNLOADS_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Downloads"
)

TEMP_FILE_EXTENSIONS = (
    ".crdownload",
    ".tmp",
    ".part",
)

TEMP_FILE_PREFIXES = (
    "~$",
    ".",
)

# Wait time after detecting a file
FILE_READY_DELAY = 1
DUPLICATE_EVENT_WINDOW = 5
FILE_READY_TIMEOUT = 30
FILE_READY_RETRY_DELAY = 1

# Webhook retry settings
WEBHOOK_TIMEOUT = 10
WEBHOOK_MAX_RETRIES = 4
WEBHOOK_INITIAL_DELAY = 1
WEBHOOK_BACKOFF_FACTOR = 2
