import uuid
from django.db import models


class Mockup(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]

    task_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    text = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} ({self.status})"


class MockupImage(models.Model):
    mockup = models.ForeignKey(Mockup, on_delete=models.CASCADE, related_name='images')
    shirt_color = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shirt_color} for {self.mockup.text}"
