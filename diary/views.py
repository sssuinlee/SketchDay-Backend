from rest_framework.response import Response
from rest_framework import status
from .models import Diary, DiaryImg, Emotion, Weather
from account.models import User
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view
from django.db.models import functions
from .serializers import DiaryListsSerializer
import itertools
from operator import itemgetter

# ml 서버로 request 전송하기
# https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
import requests
from PIL import Image
from io import BytesIO

# S3
import boto3

## env
from django.conf import settings


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('GET',))
def diary_lists(request):
    if (request.method == 'GET'):
        if(request.user.is_authenticated):
            user_id = request.user.user_id
            res_data_raw = Diary.objects.filter(user_id = user_id) \
                .extra(select={'year_month': "DATE_FORMAT(created_at, '%%Y-%%m')"}) \
                .values('year_month', 'diary_id', 'image_url')
            serializer = DiaryListsSerializer(res_data_raw, many=True)
            res_data_json = serializer.data
            sorted_data = sorted(res_data_json, key=itemgetter('year_month'))
            grouped_data = itertools.groupby(sorted_data, key=itemgetter('year_month'))
            res = {}
            for key, group_data in grouped_data:
                res[key] = list(group_data)
            return Response({'message' : '조회에 성공하였습니다.', 'data' : res}, status=status.HTTP_200_OK)
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_403_FORBIDDEN)


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('POST',))
def diary_create(request):
    if (request.method == 'POST'):
        # postman crsf 오류 해결되면 not 없애야 함
        if(not request.user.is_authenticated):
            try:
                # user_id = request.user.user_id
                user_id = request.data['user_id']
                title = request.data['title']
                content = request.data['content']
                # image_url = request.POST['image_url']
                wea_id = request.data['wea_id']
                emo_id = request.data['emo_id']
                user = User.objects.get(user_id=user_id)
                emo = Emotion.objects.get(emo_id=emo_id)
                wea = Weather.objects.get(wea_id=wea_id)
                diary = Diary.objects.create(title=title, content=content, emo_id=emo, wea_id=wea, user_id=user)
                
                prompt = send_summary_req(content)
                # DiaryImg.objects.create(prompt=prompt, diary_id=diary)
                
                return Response({'message' : '일기 저장을 성공하였습니다.', 'diary_id' : diary.diary_id}, status=status.HTTP_200_OK)
            except:
                return Response({'err_msg' : '서버 오류로 일기 저장을 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_403_FORBIDDEN)


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('PATCH',))
def diary_update(request):
    if (request.method == 'PATCH'):
        # postman crsf 오류 해결되면 not 없애야 함
        if(not request.user.is_authenticated):
            try:
                diary_id = request.data['id']
                new_content = request.data['new_content']
                diary = Diary.objects.get(diary_id=diary_id)
                diary.content = new_content
                diary.save()
                return Response({'message' : '일기 수정을 성공하였습니다.', 'diary_id' : diary.diary_id}, status=status.HTTP_200_OK)
            except:
                return Response({'err_msg' : '서버 오류로 일기 수정을 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_403_FORBIDDEN)


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('POST',))
def create_img(request):
    if (request.method == 'PATCH'):
        if(not request.user.is_authenticated):
            try:
                diary_id = request.data['id']
                diary = Diary.objects.get(diary_id=diary_id)
                diary_img = DiaryImg.objects.get(diary_id=diary)
                prompt = diary_img.prompt
                url = send_img_create_req(prompt)
                diary.image_url = url
                return Response({'message' : '그림 생성을 성공하였습니다.', 'url' : url}, status=status.HTTP_200_OK)
            except:
                return Response({'err_msg' : '서버 오류로 일기 수정을 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_403_FORBIDDEN)
                
                

# 사용자가 일기 create할 때 호출하여 ml 서버로 request 전송, 응답으로 prompt 받음
def send_summary_req(full_diary):
    res = requests.post('http://localhost:8000/ml/summaryDiary/', data = {'full_diary' : full_diary})
    print('res :', res)
    print('res.content', res.content)
    print('res.statuscode :', res.status_code)
    print('res.json :', res.json)
    print('res.text :', res.text)
    prompt = res.content
    return prompt # prompt


# 사용자가 일기 modify할 때 호출하여 ml 서버로 request 전송 
# -> url 응답 받고 반환하여 DB에 저장
# -> 프론트엔드한테 이미지 url 전송
def send_img_create_req(prompt):
    res = requests.post('http://localhost:8000/ml/generateImage/', data = {'prompt' : prompt})
    url = res.content
    return url


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('DELETE',))        
def diary_del(request):
    if (request.method == 'DELETE'):
        if(not request.user.is_authenticated):
            diary_id = request.data['id']
            try:
                target_diary = Diary.objects.get(diary_id=diary_id)
                target_diary.delete()
                return Response({'message' : '일기 삭제를 성공하였습니다.'}, status=status.HTTP_200_OK)
            except:
                return Response({'err_msg' : '서버 오류로 일기 삭제를 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'})
    
@csrf_exempt
@api_view(('PUT',))      
def get_s3_presigned_url(request):
    if (request.method == 'PUT'):
        AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', 'AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', 'AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'AWS_STORAGE_BUCKET_NAME')
        AWS_S3_CUSTOM_DOMAIN = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'AWS_S3_CUSTOM_DOMAIN')

        client = boto3.client('s3',
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                           region_name='ap-northeast-2')
        print(client)
        s3 = boto3.resource('s3')
        buckets = s3.Bucket(name=AWS_STORAGE_BUCKET_NAME)
        print(buckets)
        url = client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': 'test.txt',
            },
            # url 생성 후 10초가 지나면 접근 불가
            ExpiresIn=3600
        )
        print(url)
    
    return Response({'s3_url' : url})
