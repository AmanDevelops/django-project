from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views import *

urlpatterns = [
    path("", Public.as_view(), name="public"),
    path("protected/", Private.as_view(), name="protected"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("send_email/", send_email, name="send-email"),
    path("webhook", handle_username, name="telegram_webhook")
]
