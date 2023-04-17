from rest_framework import serializers
from .models import UserManager

class UserSerializer(serializers.Serializer):

    class Diary:
        model = UserManager
        fields = ["diary_id", "user_id", "wea_id", "emo_id", 'title', 'content', 'image_url','created_at', 'updated_at']
