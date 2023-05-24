from rest_framework.response import Response
from rest_framework import status
from .models import Diary, DiaryImg, Emotion, Weather
from account.models import User
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view
from django.db.models import functions
from .serializers import BaseDiarySerializer, DiaryListsSerializer
import itertools
from operator import itemgetter
from account.services import user_authenticate

# ml 서버로 request 전송하기
# https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
import requests


@ensure_csrf_cookie
@api_view(('GET',))
def diary_lists(request):
    if (request.method == 'GET'):
        auth_tuple = user_authenticate(request.COOKIES)
        try:
            if(auth_tuple[0]):
                user_id = auth_tuple[1]['user_id']
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
                response = Response({'message' : '조회에 성공하였습니다.', 'data' : res}, status=status.HTTP_200_OK)
                if(len(auth_tuple)==4):
                    response.set_cookie("access_token", auth_tuple[2], httponly=True)
                    response.set_cookie("refresh_token", auth_tuple[3], httponly=True)
                return response
            
            else:
                if(len(auth_tuple)==2):
                    return Response({'message' : auth_tuple[1]}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ensure_csrf_cookie
@api_view(('POST',))
def diary_create(request):
    if (request.method == 'POST'):
        auth_tuple = user_authenticate(request.COOKIES)
        try:
            if(auth_tuple[0]):
                user_id = auth_tuple[1]['user_id']
                title = request.data['title']
                content = request.data['content']
                wea_id = request.data['wea_id']
                emo_id = request.data['emo_id']
                user = User.objects.get(user_id=user_id)
                emo = Emotion.objects.get(emo_id=emo_id)
                wea = Weather.objects.get(wea_id=wea_id)
                diary = Diary.objects.create(title=title, content=content, emo_id=emo, wea_id=wea, user_id=user)
                
                prompt = send_summary_req(content)
                # DiaryImg.objects.create(prompt=prompt, diary_id=diary)

                response = Response({'message' : '일기 저장을 성공하였습니다.', 'diary_id' : diary.diary_id}, status=status.HTTP_200_OK)
                if(len(auth_tuple)==4):
                    response.set_cookie("access_token", auth_tuple[2], httponly=True)
                    response.set_cookie("refresh_token", auth_tuple[3], httponly=True)
                return response

            else:
                if(len(auth_tuple)==2):
                    return Response({'message' : auth_tuple[1]}, status=status.HTTP_400_BAD_REQUEST)   
                return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@ensure_csrf_cookie
@api_view(('GET',))
def diary_one(request, diaryId):
    if(request.method == 'GET'):
        auth_tuple = user_authenticate(request.COOKIES)
        try:
            if(auth_tuple[0]):
                    diary_id = diaryId
                    diary = Diary.objects.filter(diary_id=diary_id).values('diary_id', 'title', 'content', 'emo_id', 'wea_id', 'image_url')
                    serializer = BaseDiarySerializer(diary, many=True)                    
                    res = serializer.data
                    response = Response({'message' : '일기 조회를 성공하였습니다.', 'res':res}, status=status.HTTP_200_OK)
                    
                    if(len(auth_tuple) == 4):
                        response.set_cookie("access_token", auth_tuple[2], httponly=True)
                        response.set_cookie("refresh_token", auth_tuple[3], httponly=True)
                    return response
                
            else:
                    if(len(auth_tuple)==2):
                        return Response({'message' : auth_tuple[1]}, status=status.HTTP_400_BAD_REQUEST)   
                    return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
                
            
                
                
@ensure_csrf_cookie
@api_view(('PATCH',))
def diary_update(request):
    if (request.method == 'PATCH'):
        auth_tuple = user_authenticate(request.COOKIES)
        try:
            if(auth_tuple[0]):
                diary_id = request.GET['id']
                new_content = request.data['new_content']
                diary = Diary.objects.get(diary_id=diary_id)
                diary.content = new_content
                diary.save()
                response = Response({'message' : '일기 수정을 성공하였습니다.', 'diary_id' : diary.diary_id}, status=status.HTTP_200_OK)
                if(len(auth_tuple)==4):
                    response.set_cookie("access_token", auth_tuple[2], httponly=True)
                    response.set_cookie("refresh_token", auth_tuple[3], httponly=True)
                return response

            else:
                if(len(auth_tuple)==2):
                    return Response({'message' : auth_tuple[1]}, status=status.HTTP_400_BAD_REQUEST)   
                return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@ensure_csrf_cookie
@api_view(('POST',))
def create_img(request):
    return

# 사용자가 일기 create할 때 호출하여 ml 서버로 request 전송, 응답으로 prompt 받음
def send_summary_req(full_diary):
    res = requests.post('http://localhost:8000/ml/summaryDiary/', data = {'full_diary' : full_diary})
    print('res :', res)
    print('res.content', res.content)
    print('res.statuscode :', res.status_code)
    print('res.json :', res.json)
    print('res.text :', res.text)
    return res.content # prompt


# 사용자가 일기 modify할 때 호출하여 ml 서버로 request 전송 
# -> 응답 받고 S3에 이미지 저장, url 반환하여 DB에 저장 
# -> 사용자에게 이미지 url 전송 
def send_img_create_req(prompt):
    res = requests.post('http://localhost:8000/ml/generateImage/', data = {'prompt' : prompt})
    # res가 binary여야 함
    # 이미지 오픈
    i = Image.open(BytesIO(res.content))
    
    # 이미지 S3에 저장, url DB에 저장하는 로직
    
    url = ''
    return url


@ensure_csrf_cookie
@api_view(('DELETE',))        
def diary_del(request):
    if (request.method == 'DELETE'):
        auth_tuple = user_authenticate(request.COOKIES)
        try:
            if(auth_tuple[0]):
                diary_id = request.GET['id']
                target_diary = Diary.objects.get(diary_id=diary_id)
                target_diary.delete()
                response = Response({'message' : '일기 삭제를 성공하였습니다.'}, status=status.HTTP_200_OK)
                if(len(auth_tuple)==4):
                    response.set_cookie("access_token", auth_tuple[2], httponly=True)
                    response.set_cookie("refresh_token", auth_tuple[3], httponly=True)
                return response

            else:
                if(len(auth_tuple)==2):
                    return Response({'message' : auth_tuple[1]}, status=status.HTTP_400_BAD_REQUEST)   
                return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({'err_msg' : '서버 오류입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


