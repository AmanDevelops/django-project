from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views import *

urlpatterns = [
    path("", Public.as_view(), name="public"),  # Public API view - accessible by anyone
    path(
        "protected/", Private.as_view(), name="protected"
    ),  # Private API view - requires JWT token authentication
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT token pair obtain route - returns access and refresh tokens
    path(
        "send_email/", send_email, name="send-email"
    ),  # Route to trigger an email via Celery task
    path(
        "webhook", handle_username, name="telegram_webhook"
    ),  # Telegram webhook endpoint - expects POST requests from Telegram bot
]
