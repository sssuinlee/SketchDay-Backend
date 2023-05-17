from django.db import models
import uuid

class Weather(models.Model):
    wea_id = models.IntegerField(primary_key=True)
    wea_state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.wea_state

class Emotion(models.Model):
    emo_id = models.IntegerField(primary_key=True)
    emo_state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.emo_state
    
class Diary(models.Model):
    diary_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE, default='') # account app의 User 참조, diary_diary_user_id라는 중간 테이블 생김
    wea_id = models.ForeignKey(Weather, on_delete=models.PROTECT)
    emo_id = models.ForeignKey(Emotion, on_delete=models.PROTECT)
    title = models.CharField(max_length=120, null=True, default='')
    content = models.CharField(max_length=255, null=False)
    image_url = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class DiaryImg(models.Model):
    diary_img_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE, null=False)
    prompt = models.CharField(max_length=1000, null=False)
    url = models.TextField(null=True)
    thumbnail_url = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt