from celery import shared_task

from apps.utils.logging.logger import new_logger


logger = new_logger()


@shared_task
def log_debug(message, properties):
    logger.warn(message=message, properties=properties)


@shared_task
def log_info(message, properties):
    logger.info(message=message, properties=properties)


@shared_task
def log_warn(message, properties):
    logger.warn(message=message, properties=properties)


@shared_task
def log_error(message, properties):
    logger.error(message=message, properties=properties)
