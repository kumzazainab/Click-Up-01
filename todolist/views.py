from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.permissions import IsAdminOrProjectManager
from todolist.task import stop_timer

class StopTimerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        stop_timer.delay()
        return Response({"message": "Timer stop task triggered successfully!"}, status=status.HTTP_200_OK)