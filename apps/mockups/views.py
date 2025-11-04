from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from .models import Mockup
from .serializers import MockupSerializer
from .tasks import generate_mockup_images_task


class GenerateMockupAPIView(APIView):
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
    def get(self, request, task_id):
        mockup = get_object_or_404(Mockup, task_id=task_id)
        serializer = MockupSerializer(mockup)
        return Response(serializer.data)


class MockupListAPIView(generics.ListAPIView):
    queryset = Mockup.objects.all().order_by('-created_at')
    serializer_class = MockupSerializer