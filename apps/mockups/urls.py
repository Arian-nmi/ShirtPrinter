from django.urls import path
from .views import SignupAPIView, GenerateMockupAPIView, TaskStatusAPIView, MockupListAPIView


urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('generate/', GenerateMockupAPIView.as_view()),
    path('tasks/<uuid:task_id>/', TaskStatusAPIView.as_view()),
    path('', MockupListAPIView.as_view()),
]