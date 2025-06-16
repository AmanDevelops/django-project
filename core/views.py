import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.task import send_welcome_email

from core.models import UserData


class Public(APIView):
    permission_classes = []

    def get(self, request):
        data = {"message": "Hello From AmanDevelops"}
        return Response(data, status=status.HTTP_200_OK)


class Private(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"message": "This is a super Secret Message"}
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def send_email(request):
    user_email = request.GET.get("email")
    if not user_email:
        data = {"message": "At least one email address is required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    send_welcome_email.delay(user_email)
    return Response({"message": "Email Sent Successfully"})


@api_view(["POST"])
@csrf_exempt
def handle_username(request):
    if request.method == "POST":
        try:
            request_data = request.body.decode("utf-8")
            data = json.loads(request_data)
            message = data.get("message").get("text")
            if "/start" in message:
                username = data.get("message").get("from").get("username")
                if not UserData.objects.filter(telegram_username=username).exists():
                    user_data = UserData(telegram_username=username)
                    user_data.save()

        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError:
            return Response({"message": "Response accepted from Telegram Webhook Only"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return Response(status=status.HTTP_200_OK)
