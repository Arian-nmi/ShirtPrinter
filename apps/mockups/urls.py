from django.urls import path
from .views import GenerateMockupAPIView, TaskStatusAPIView, MockupListAPIView


urlpatterns = [
    path('generate/', GenerateMockupAPIView.as_view()),
    path('tasks/<uuid:task_id>/', TaskStatusAPIView.as_view()),
    path('', MockupListAPIView.as_view()),
]