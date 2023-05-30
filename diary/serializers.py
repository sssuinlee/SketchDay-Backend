from rest_framework import serializers
from .models import Diary

class BaseDiarySerializer(serializers.Serializer):
    diary_id = serializers.UUIDField()
    date = serializers.DateField()
    content = serializers.CharField(max_length=255)
    emo_id = serializers.IntegerField()
    wea_id = serializers.IntegerField()
    image_url = serializers.CharField(max_length=200)
    
    def create(self, **validated_data):
        return Diary.create(**validated_data)

class DiaryListsSerializer(serializers.Serializer):
    year_month = serializers.DateField()
    diary_id = serializers.UUIDField()
    image_url = serializers.CharField(max_length=200)
    
    def create(self, **validated_data):
        return Diary.create('year_month', 'diary_id', 'image_url')