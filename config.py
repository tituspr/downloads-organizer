import os
import json
from pathlib import Path

from logger import logger

CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "notifications": True,
    "startup_delay": 3,
    "organize_delay": 0,
}

_config = None

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


def load_config():

    """Load configuration from config.json."""
    
    global _config

    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG.copy())

        logger.warning(
            "Configuration file not found. Created default configuration."
        )
        return _config

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)

    except (json.JSONDecodeError, OSError):
        save_config(DEFAULT_CONFIG.copy())
        _config = DEFAULT_CONFIG.copy()

        logger.warning(
            "Configuration file is invalid. Restored default configuration."
        )
        return _config

    updated = False

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            updated = True

    if updated:
        save_config(config)
        logger.info(
            "Configuration updated with new default settings."
        )

    _config = config

    logger.info(
        "Configuration loaded from %s",
        CONFIG_FILE
    )

    return _config


def save_config(config):
    """Save configuration to config.json."""

    global _config
    _config = config

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def get_config(key):
    """Return a configuration value."""

    global _config

    if _config is None:
        load_config()

    return _config.get(key)


def set_config(key, value):
    """Update a configuration value and save it."""

    global _config

    if _config is None:
        load_config()

    _config[key] = value
    save_config(_config)


