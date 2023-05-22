from rest_framework import serializers
from .models import Diary

class BaseDiarySerializer(serializers.Serializer):
    class Meta:
        model = Diary
        fields = ["diary_id", "user_id", "wea_id", "emo_id", 'title', 'content', 'image_url','created_at', 'updated_at']

class DiaryListsSerializer(serializers.Serializer):
    year_month = serializers.DateField()
    diary_id = serializers.UUIDField()
    image_url = serializers.CharField(max_length=200)
    
    def create(self, **validated_data):
        return Diary.create('year_month', 'diary_id', 'image_url')