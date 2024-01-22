import time

from apps.utils.logging.logger import get_logger, get_request_response_properties

logger = get_logger()


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()

        response_time = round((end_time - start_time) * 1000)

        properties = get_request_response_properties(response_time=f"{response_time}ms", method=request.method,
                                                     status_code=response.status_code, path=request.path)
        logger.info(message=f"[{request.method}:{response.status_code}] {request.path} | {response_time}ms",
                    properties=properties)

        return response
