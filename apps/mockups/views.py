from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Mockup
from .serializers import MockupSerializer
from .tasks import generate_mockup_images_task


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class GenerateMockupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        text = request.data.get("text")
        if not text:
            return Response({"error": "Text field is required."}, status=status.HTTP_400_BAD_REQUEST)

        mockup = Mockup.objects.create(text=text, status="PENDING")
        generate_mockup_images_task.delay(str(mockup.task_id))

        return Response({
            "task_id": str(mockup.task_id),
            "status": "PENDING",
            "message": "Generating image has started ..."
        }, status=status.HTTP_202_ACCEPTED)


class TaskStatusAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, task_id):
        mockup = get_object_or_404(Mockup, task_id=task_id)
        serializer = MockupSerializer(mockup)
        return Response(serializer.data)


class MockupListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mockup.objects.all().order_by('-created_at')
    serializer_class = MockupSerializer