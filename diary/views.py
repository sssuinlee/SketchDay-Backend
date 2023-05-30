from rest_framework.response import Response
from rest_framework import status
from .models import Diary, DiaryImg, Emotion, Weather
from account.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import BaseDiarySerializer, DiaryListsSerializer
import itertools
from operator import itemgetter
import boto3
from .services import send_img_create_req, send_summary_req
import backend.config.settings.base as settings
import requests


# S3
import boto3

## env
from django.conf import settings



@ensure_csrf_cookie
@api_view(('GET',))
@permission_classes([IsAuthenticated])
def diary_lists(request):
    if (request.method == 'GET'):
        try:
            user = request.user
            user_id = user.user_id
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
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([IsAuthenticated])
def diary_create(request):
    if (request.method == 'POST'):
        try:
            user = request.user
            user_id = user.user_id
            title = request.data['title']
            content = request.data['content']
            wea_id = request.data['wea_id']
            emo_id = request.data['emo_id']
            user = User.objects.get(user_id=user_id)
            emo = Emotion.objects.get(emo_id=emo_id)
            wea = Weather.objects.get(wea_id=wea_id)
            diary = Diary.objects.create(title=title, content=content, emo_id=emo, wea_id=wea, user_id=user)
                
            # ml 서버로 request 전송, 응답으로 prompt 받음
            prompt = send_summary_req(content)
            DiaryImg.objects.create(prompt=prompt, diary_id=diary)

            return Response({'message' : '일기 저장을 성공하였습니다.', 'diary_id' : diary.diary_id}, status=status.HTTP_200_OK)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@ensure_csrf_cookie
@api_view(('GET',))
@permission_classes([IsAuthenticated])
def diary_one(request, diaryId):
    if(request.method == 'GET'):
        try:
            diary_id = diaryId
            diary = Diary.objects.filter(diary_id=diary_id).values('diary_id', 'title', 'content', 'emo_id', 'wea_id', 'image_url')
            serializer = BaseDiarySerializer(diary, many=True)                    
            res = serializer.data
            
            return Response({'message' : '일기 조회를 성공하였습니다.', 'res':res}, status=status.HTTP_200_OK)
     
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
                
            
                
@ensure_csrf_cookie
@api_view(('PATCH',))
@permission_classes([IsAuthenticated])
def diary_update(request):
    if (request.method == 'PATCH'):
        try:
            diary_id = request.GET['id']
            new_content = request.data['new_content']
            diary = Diary.objects.get(diary_id=diary_id)
            diary.content = new_content
            diary.save()

            return Response({'message' : '일기 수정을 성공하였습니다.', 'diary_id' : diary.diary_id}, status=status.HTTP_200_OK)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([IsAuthenticated])
def create_img(request):
    if (request.method == 'PATCH'):
        try:
            diary_id = request.GET['id']
            diary = Diary.objects.get(diary_id=diary_id)
            diary_img = DiaryImg.objects.get(diary_id=diary)
            prompt = diary_img.prompt
            url = send_img_create_req(prompt)
            diary.image_url = url
       
            return Response({'message' : '그림 생성을 성공하였습니다.', 'url' : url}, status=status.HTTP_200_OK)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ensure_csrf_cookie
@api_view(('DELETE',))   
@permission_classes([IsAuthenticated])     
def diary_del(request):
    if (request.method == 'DELETE'):
        try:
            diary_id = request.GET['id']
            target_diary = Diary.objects.get(diary_id=diary_id)
            target_diary.delete()
            
            return Response({'message' : '일기 삭제를 성공하였습니다.'}, status=status.HTTP_200_OK)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
@ensure_csrf_cookie
@api_view(('PUT',))
@permission_classes([IsAuthenticated])    
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
        
        # presigned URL 생성
        url = client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': 'test.txt',
            },
            # url 생성 후 10초가 지나면 접근 불가
            ExpiresIn=3600
        )
        
        # 이미지 파일 업로드
        # s3 = boto3.resource('s3')
        # s3.Object(AWS_STORAGE_BUCKET_NAME, 'image.jpg').upload_fileobj(image_file)
        
        print(url)
    
    return Response({'s3_url' : url})



#######################################################################

from .services import send_img

@ensure_csrf_cookie
@api_view(('POST',))
def diary_uploadImg(request):
    if (request.method == 'POST'):
        try:
            user = request.user
            user_id = user.user_id
            user = User.objects.get(user_id=user_id)

            # 이미지 파일 받기
            image_file = request.FILES.get('image')
            if image_file is None:
                return Response({'error': '이미지 파일이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # presigned URL에 이미지 저장
            print("presigned URL에 이미지 저장 전:", image_file) ### debug
            url = send_img(image_file)
            print("presigned URL에 이미지 저장 후:", url)        ### debug
            
            return Response({'url': url}, status=status.HTTP_200_OK)

        except:
            return Response({'error': 'URL에 이미지를 저장하는데 실패했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)