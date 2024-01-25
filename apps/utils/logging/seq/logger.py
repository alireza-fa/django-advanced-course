from typing import Dict
import requests
from django.utils import timezone

from apps.utils.logging.base import Log
from .urls import NEW_EVENT
from apps.utils.logging import log_level


class SeqDataLust(Log):

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def debug(self, message: str, properties: Dict):
        self.create_new_event(level=log_level.DEBUG, message=message, properties=properties)

    def info(self, message: str, properties: Dict):
        self.create_new_event(level=log_level.INFO, message=message, properties=properties)

    def warn(self, message: str, properties: Dict):
        self.create_new_event(level=log_level.WARN, message=message, properties=properties)

    def error(self, message: str, properties: Dict):
        self.create_new_event(level=log_level.ERROR, message=message, properties=properties)

    def create_new_event(self, level: int, message: str, properties: Dict):
        data = {
            "Events": [
                {
                    "Level": level,
                    "MessageTemplate": message,
                    "Timestamp": str(timezone.now()),
                    "Properties": {
                        **properties
                    }
                }
            ]
        }
        requests.post(url=self.base_url + NEW_EVENT, headers={"X-Seq-ApiKey": "6CGsArH5o6q1jGeP0vsz"}, json=data)
