import os
import logging

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler("logs/organizer.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("DownloadsOrganizer")