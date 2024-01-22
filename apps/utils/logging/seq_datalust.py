import requests
from django.utils import timezone
from django.conf import settings

from .base import Log
from . import log_level


BASE_URL = settings.SEQ_URL
EVENT_URL = BASE_URL + "/api/events/raw"


class SeqDataLust(Log):

    def __init__(self, api_key: str):
        self.api_key = api_key

    def debug(self, message: str, category: str, sub_category: str):
        return self.create_new_event(message, level=log_level.DEBUG,
                                     category=category, sub_category=sub_category)

    def info(self, message: str, category: str, sub_category: str):
        return self.create_new_event(message=message, level=log_level.INFO,
                                     category=category, sub_category=sub_category)

    def warn(self, message: str, category: str, sub_category: str):
        return self.create_new_event(message=message, level=log_level.WARN,
                                     category=category, sub_category=sub_category)

    def error(self, message: str, category: str, sub_category: str):
        return self.create_new_event(message=message, level=log_level.ERROR,
                                     category=category, sub_category=sub_category)

    @staticmethod
    def create_new_event(message, level, category, sub_category):
        print(EVENT_URL)
        data = {
            "Events": [
                {
                    "Level": level,
                    "MessageTemplate": message,
                    "Timestamp": str(timezone.now()),
                    "Properties": {"Category": category, "SubCategory": sub_category}
                }
            ]
        }
        requests.post(EVENT_URL, json=data, headers={"X-Seq-ApiKey": settings.SEQ_API_KEY})
