import logging

logger = logging.getLogger(__name__)


class LogUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy User-Agent từ request
        user_agent = request.META.get("HTTP_USER_AGENT", "unknown")

        # Ghi User-Agent vào log
        logger.info(f"User-Agent: {user_agent}")

        response = self.get_response(request)
        return response
