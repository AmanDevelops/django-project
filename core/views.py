from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *


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