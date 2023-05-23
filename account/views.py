from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from account.models import User
from .services import send_mail, email_auth_string
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view

# Error 처리 view (DEBUG = False일 경우만 동작)
def error_404_view(request, exception):
    return HttpResponseNotFound("The page is not found")

# @ensure_csrf_cookie
@csrf_exempt
@api_view(('POST',))
def login_view(request):
    if(request.method == 'POST'):
        if(request.user.is_anonymous):
            print('request', request)
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
        
            if(user is not None):
                login(request, user)
                print('user 정보:', request.user)
                return Response({'success' : '로그인에 성공하였습니다.'}, status=status.HTTP_200_OK)
    
            else:
                return Response({'err_msg' : '로그인에 실패하였습니다. 올바른 아이디와 비밀번호를 입력했는지 확인해주세요.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, 
                                status=status.HTTP_403_FORBIDDEN)
            

# @ensure_csrf_cookie
@csrf_exempt
@api_view(('GET',))
def logout_view(request):
    if(request.method == 'GET'):
        if(not request.user.is_anonymous):
            logout(request)
            return Response({'success' : '로그아웃에 성공하였습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, 
                                status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'err_msg' : '로그아웃에 실패하였습니다.'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('POST',))
def send_verification_code(request):
    if(request.method == 'POST'):
        target_email = request.POST['email']
        try:
            exist_user = User.objects.get(auth_email=target_email)
        except User.DoesNotExist:
            exist_user = None

        if(exist_user is None):
            auth_code = email_auth_string()
            cache.set(target_email, auth_code)
            print(cache.get(target_email))
            try:
                send_mail(
                    'Sketch Day 이메일 인증 코드입니다.',
                    recipient_list=[target_email],
                    html=render_to_string('inviteMailForm.html', {
                    'user_email': target_email,
                    'auth_code': auth_code,                    
                    })
                )
                return Response({'success' : '성공적으로 사용자 이메일로 인증코드를 전송하였습니다.'}, status=status.HTTP_200_OK)
            except:
                return Response({"err_msg" : "서버 혹은 네트워크 오류로 이메일 전송에 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'err_msg' : '이미 가입된 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('POST',))
def verify_code(request):
    if(request.method == 'POST'):
        verify_email = request.POST['email']
        verify_code = request.POST['verifyCode']
        cache_code = cache.get(verify_email)
        
        print(verify_email)
        print(verify_code)
        print(cache_code)
        
        if(verify_code == cache_code):
            cache.delete(verify_email)
            return Response({'success':'성공적으로 인증되었습니다.'}, status=status.HTTP_200_OK)
        
        return Response({
            'err_msg' : '잘못된 인증번호입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('POST',))
def signup_view(request):
    if(request.method == "POST"):
        if(request.user.is_anonymous):
            auth_email = request.POST['email']
            try:
                exist_user = User.objects.get(auth_email=auth_email)
            except User.DoesNotExist:
                exist_user = None

            if(exist_user is None):
                user = User.objects.create_user(
                    auth_email=auth_email,
                    password=request.POST['password'],
                    name=request.POST['name'],
                    birth=request.POST['birth'],
                )
                print(user)
                return Response({'success':'성공적으로 가입이 완료되었습니다.'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'err_msg' : '이미 가입된 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, 
                                status=status.HTTP_403_FORBIDDEN)
