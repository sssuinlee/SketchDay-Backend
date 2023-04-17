from django.db import models
import uuid

class DiaryImg(models.Model):
    diary_img_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
    diary_id = models.ForeignKey('diary.Diary', on_delete=models.CASCADE)
    prompt = models.CharField(max_length=1000, null=False)
    url = models.TextField(null=False)
    thumbnail_url = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt
    