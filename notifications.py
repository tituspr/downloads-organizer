"""
notifications.py
Handles desktop notifications for the Downloads Organizer.
"""

from plyer import notification
from config import get_config

APP_NAME = "Downloads Organizer"


class NotificationManager:

    def notify(self, title, message):

        if not get_config("notifications"):
            return

        try:
            notification.notify(
                title=title,
                message=message,
                app_name=APP_NAME,
                timeout=5,
            )
        except Exception:
            pass