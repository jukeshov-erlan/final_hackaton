import logging

logger = logging.getLogger(__name__)


class LoggingView:
    def log_user_activity(self, request, action):
        user = request.user.username
        logger.info(f"User '{user}' performed action: {action}")
