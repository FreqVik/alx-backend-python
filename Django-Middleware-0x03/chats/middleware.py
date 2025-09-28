import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from collections import defaultdict
import time


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
    

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app
    between 21:00 and 18:00.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        gets the current hour
        """
        current_hour = datetime.now().hour
        """
        Restrict access between 21:00 and 18:00.
        """
        if current_hour > 18 and current_hour < 21:
            return HttpResponseForbidden("Access to the messaging app is restricted during this time.")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that limits chat messages per IP address.
    A user (by IP) can only send 5 messages per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = defaultdict(list)
        self.limit = 5
        self.time_window = 60
    def __call__(self, request):
        """
        Limit chat messages per IP address.
        A user (by IP) can only send 5 messages per minute.
        """
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up timestamps older than 1 min
            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip] if now - t < self.time_window
            ]

            if len(self.ip_requests[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded: You can only send 5 messages per minute."
                )
            # Log this request
            self.ip_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve client IP address from request headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    

class RolePermissionMiddleware:
    """
    Middleware that restricts access based on user role.
    Only users with role = 'admin' or 'moderator' are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only run check if user is authenticated
        if hasattr(request, "user") and request.user.is_authenticated:
            # Assuming your custom User model has a `role` field
            user_role = getattr(request.user, "role", None)

            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "Access denied: only admins and moderators are allowed."
                )

        return self.get_response(request)
    

class RolePermissionMiddleware:
    """
    Middleware that restricts access based on user role.
    Only users with role = 'admin' or 'moderator' are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Only run check if user is authenticated
        """
        if hasattr(request, "user") and request.user.is_authenticated:
            user_role = getattr(request.user, "role", None)

            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "Access denied: only admins and moderators are allowed."
                )
        return self.get_response(request)