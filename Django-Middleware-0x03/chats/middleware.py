import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin


class RequestLoggingMiddleware:
    """
    Middleware that logs each user’s requests to a file
    with timestamp, user, and request path.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware and set up logging.
        """
        self.get_response = get_response
        
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        """
        Log the request details and continue processing.
        """
        user = (
            request.user.username
            if hasattr(request, "user") and request.user.is_authenticated
            else "Anonymous"
        )
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response
