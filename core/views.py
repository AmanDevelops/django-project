from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.task import send_welcome_email


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
