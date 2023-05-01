from django.db import models
import uuid

class Weather(models.Model):
    wea_id = models.IntegerField(),
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.state

class Emotion(models.Model):
    emo_id = models.IntegerField(),
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.state

class DiaryImg(models.Model):
    diary_img_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
    prompt = models.CharField(max_length=1000, null=False)
    url = models.TextField(null=False)
    thumbnail_url = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt
    
class Diary(models.Model):
    diary_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE) # account app의 User 참조
    wea_id = models.ForeignKey(Weather, on_delete=models.PROTECT)
    emo_id = models.ForeignKey(Emotion, on_delete=models.PROTECT)
    title = models.CharField(max_length=120),
    content = models.CharField(max_length=255)
    diary_img_id = models.ForeignKey(DiaryImg, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

