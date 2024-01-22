from django.conf import settings

from .seq_datalust import SeqDataLust
from . import category


def get_logger():
    logger_name = settings.LOGGER

    match logger_name:
        case "seq":
            return SeqDataLust(settings.SEQ_API_KEY)


def get_request_response_properties(**kwargs):
    return {
        "Category": category.RequestResponse,
        "SubCategory": category.API,
        **kwargs
    }
