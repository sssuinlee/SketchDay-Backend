from rest_framework import serializers
from .models import UserManager

class UserSerializer(serializers.Serializer):
    class Meta:
        model = UserManager
        fields = ["user_id", "auth_email", "auth_password", "name", 'created_at', 'updated_at']
