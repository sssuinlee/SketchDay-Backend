from rest_framework import serializers
from .models import DiaryImg

class DiaryImageSerializer(serializers.Serializer):
    class Meta:
        model = DiaryImg
        fields = [
            'id', 'diary_id', 'prompt', 'url', 'thumbnail_url', 'created_at', 'updated_at'
        ]
    
    def update(self, instance, updated_data):
        result = instance
        result.url = updated_data.get('url', instance.url)
        result.thumbnail_url = updated_data.get('thumbnail_url', instance.thumbnail_url)
        result.save()
        return result
