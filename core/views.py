import json
import re

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import UserData
from core.task import send_welcome_email


class Public(APIView):
    """
    Public API view.

    Returns a simple greeting message.
    No authentication required.
    """

    permission_classes = []

    def get(self, request):
        data = {"message": "Hello From AmanDevelops"}
        return Response(data, status=status.HTTP_200_OK)


class Private(APIView):
    """
    Private API view.

    Returns a protected message.
    JWT authentication is required.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"message": "This is a super Secret Message"}
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def send_email(request):
    """
    Send Welcome Email (async via Celery)

    Query Params:
        - email (str): Recipient's email address.

    Returns:
        - 200 OK: If email task was queued successfully.
        - 400 Bad Request: If no email was provided.
    """
    user_email = request.GET.get("email")
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # if user did not provide any email
    if not user_email:
        data = {"message": "At least one email address is required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    # if provided text is not a valid email address
    if re.match(pattern, user_email) is None:
        data = {"message": "Please provide a valid email address"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    try:
        send_welcome_email.delay(user_email)
        return Response({"message": "Email Sent Successfully"})
    except:
        # Handling Connection Error to redis server
        error_message = {"message": "Something went wrong!"}
        return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def handle_username(request):
    """
    Telegram Webhook Handler

    Expects JSON payload from Telegram. If the `/start` command is present
    in the message, it stores the sender's Telegram username in the DB.

    Returns:
        - 200 OK: For successful or no-op responses.
        - 400 Bad Request: If JSON is invalid or payload is malformed.
    """

    try:
        # takes the given data and sanitize it
        data = json.loads(request.body.decode("utf-8"))

        # checks if user sent /start command
        if "/start" in data.get("message", {}).get("text", ""):
            username = data.get("message", {}).get("from", {}).get("username")

            # checks if user does not exists 
            if not UserData.objects.filter(telegram_username=username).exists():
                user_data = UserData(telegram_username=username)
                user_data.save()

    except json.JSONDecodeError:
        #handling unsanitized input
        return Response({"message": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    except (AttributeError, TypeError, KeyError):
        # handling non telegram inputs
        return Response(
            {"message": "Malformed payload — expected Telegram webhook format"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(status=status.HTTP_200_OK)
