from django.conf import settings

from .seq_datalust import SeqDataLust


def get_logger():
    logger_name = settings.LOGGER

    match logger_name:
        case "seq":
            return SeqDataLust(settings.SEQ_API_KEY)
