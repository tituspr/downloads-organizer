import requests

from logger import logger
from config import WEBHOOK_URL

from requests.exceptions import (
    ConnectionError,
    Timeout,
    RequestException
)


def classify_file(payload: dict) -> str:

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

        return destination

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

    return None