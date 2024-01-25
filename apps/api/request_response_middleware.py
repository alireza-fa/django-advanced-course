import time

from apps.utils.logging.logger import new_logger
from apps.utils.logging import category


logger = new_logger()


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()

        response_time = round((end_time - start_time) * 1000)

        properties = {
            "Category": category.RequestResponse,
            "SubCategory": category.API,
            "Method": request.method,
            "ResponseTime": response_time,
            "Path": request.path,
            "StatusCode": response.status_code
        }
        logger.info(
            message=f"[{request.method}] {request.path} | {response_time}ms",
            properties=properties
        )

        return response
