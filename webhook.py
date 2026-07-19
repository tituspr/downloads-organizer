import requests
import time
from typing import Optional

from logger import logger

from config import (
    WEBHOOK_URL,
    WEBHOOK_TIMEOUT,
    WEBHOOK_MAX_RETRIES,
    WEBHOOK_INITIAL_DELAY,
    WEBHOOK_BACKOFF_FACTOR
)

from requests.exceptions import (
    ConnectionError,
    Timeout,
    RequestException
)


def classify_file(payload: dict) -> Optional[str]:

    try:

        response = call_webhook(payload)

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


def call_webhook(payload: dict) -> requests.Response:

    delay = WEBHOOK_INITIAL_DELAY

    for attempt in range(1, WEBHOOK_MAX_RETRIES + 1):

        try:

            logger.info(
                f"Sending webhook (Attempt {attempt}/{WEBHOOK_MAX_RETRIES})"
            )

            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                timeout=WEBHOOK_TIMEOUT
            )

            response.raise_for_status()

            if attempt > 1:
                logger.info(
                    f"Webhook succeeded on attempt {attempt}/{WEBHOOK_MAX_RETRIES}."
                )

            return response

        except (ConnectionError, Timeout, RequestException) as e:

            logger.warning(
                f"Attempt {attempt}/{WEBHOOK_MAX_RETRIES} failed: {e}"
            )

            if attempt == WEBHOOK_MAX_RETRIES:
                raise

            logger.info(f"Retrying in {delay} second(s)...")

            time.sleep(delay)

            delay *= WEBHOOK_BACKOFF_FACTOR