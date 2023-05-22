from rest_framework import serializers
from .models import User

class BaseUserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    auth_email = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=30)
    birth = serializers.DateField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    def create(self, **validated_data):
        return User.create(**validated_data)

class UserInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    auth_email = serializers.CharField(max_length=50)
    birth = serializers.DateField()
    
    def create(self, **validated_data):
        return User.create(**validated_data)