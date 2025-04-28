from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.permissions import IsAdminOrProjectManager
from todolist.task import stop_timer
from todolist.utils import get_greeting_message


class StopTimerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        stop_timer.delay()
        return Response({"message": "Timer stop task triggered successfully!"}, status=status.HTTP_200_OK)


class GreetingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_name = request.user.first_name or request.user.username
        message = get_greeting_message(user_name)
        return Response({"greeting": message})