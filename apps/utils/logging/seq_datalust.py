from typing import Dict
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

    def debug(self, message: str, properties: Dict):
        return self.create_new_event(message, level=log_level.DEBUG, properties=properties)

    def info(self, message: str, properties: Dict):
        return self.create_new_event(message=message, level=log_level.INFO, properties=properties)

    def warn(self, message: str, properties: Dict):
        return self.create_new_event(message=message, level=log_level.WARN, properties=properties)

    def error(self, message: str, properties: Dict):
        return self.create_new_event(message=message, level=log_level.ERROR, properties=properties)

    @staticmethod
    def create_new_event(message: str, level: str, properties: Dict):
        print(EVENT_URL)
        data = {
            "Events": [
                {
                    "Level": level,
                    "MessageTemplate": message,
                    "Timestamp": str(timezone.now()),
                    "Properties": {**properties}
                }
            ]
        }
        requests.post(EVENT_URL, json=data, headers={"X-Seq-ApiKey": settings.SEQ_API_KEY})
