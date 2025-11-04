from rest_framework import serializers
from .models import Mockup, MockupImage


class MockupImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockupImage
        fields = ['shirt_color', 'image_url', 'created_at']


class MockupSerializer(serializers.ModelSerializer):
    images = MockupImageSerializer(many=True, read_only=True)

    class Meta:
        model = Mockup
        fields = ['task_id', 'text', 'status', 'created_at', 'images']
