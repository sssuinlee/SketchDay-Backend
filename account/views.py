from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from account.models import User
from .services import send_mail, email_auth_string
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserLoginAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        try: 
            user = User.objects.get(auth_email=email)
        except User.DoesNotExist:
            user = None

        # 만약 username에 맞는 user가 존재하지 않는다면,
        if user is None:
            return Response(
                {"err_message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 틀린 경우,
        if not user.check_password(password):
            return Response(
                {"err_message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        # user가 맞다면,
        if user is not None:
            print(user)
            token = TokenObtainPairSerializer.get_token(user) # refresh 토큰 생성
            refresh_token = str(token) # refresh 토큰 문자열화
            access_token = str(token.access_token) # access 토큰 문자열화
            response = Response(
                {
                    "success": "로그인에 성공하였습니다.",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLogoutAPI(APIView):
    def post(self, request):
        if(request.user.is_authenticated):
            response = Response({
                'message' : 'Logout Success'
            }, status=status.HTTP_200_OK)

            return response
        else:
            return Response({'detail' : "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([AllowAny])
def signup_send_verification_code(request):
    if(request.method == 'POST'):
        target_email = request.data['email']
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
                return Response({'success' : '성공적으로 인증코드를 전송하였습니다.'}, status=status.HTTP_200_OK)
            except:
                return Response({"err_msg" : "서버 혹은 네트워크 오류로 이메일 전송에 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'err_msg' : '이미 가입된 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([AllowAny])
def signup_verify_code(request):
    if(request.method == 'POST'):
        try:
            verify_email = request.data['email']
            verify_code = request.data['verifyCode']
            cache_code = cache.get(verify_email)
            
            print(verify_email)
            print(verify_code)
            print(cache_code)
            
            if(verify_code == cache_code):
                cache.delete(verify_email)
                return Response({'success':'성공적으로 인증되었습니다.'}, status=status.HTTP_200_OK)
            
            return Response({'err_msg' : '잘못된 인증번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({"err_msg" : "인증을 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([AllowAny])
def signup_view(request):
    if(request.method == "POST"):
        try:
            auth_email = request.data['email']
            try:
                exist_user = User.objects.get(auth_email=auth_email)
            except User.DoesNotExist:
                exist_user = None

            if(exist_user is None):
                user = User.objects.create_user(
                    auth_email=auth_email,
                    password=request.data['password'],
                    name=request.data['name'],
                    birth=request.data['birth'],
                )
                print(user)
                return Response({'success':'성공적으로 가입이 완료되었습니다.'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'err_msg' : '이미 가입된 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"err_msg" : "서버 오류로 회원가입에 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([AllowAny])
def find_password_send_verification_code(request):
    if(request.method == 'POST'):
        try: 
            auth_email = request.data['email']
            name = request.data['name']
            user = User.objects.filter(auth_email=auth_email, name=name)
         
            if (len(user) == 0):
                raise User.DoesNotExist
            
            auth_code = email_auth_string()
            cache.set(auth_email, auth_code)
            
            print(cache.get(auth_email))
            
            send_mail(
                'Sketch Day 이메일 인증 코드입니다.',
                recipient_list=[auth_email],
                html=render_to_string('inviteMailForm.html', {
                'user_email': auth_email,
                'auth_code': auth_code,                   
                })
            )
            
            return Response({'success' : '성공적으로 인증코드를 전송하였습니다.'}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({'err_message' : '존재하지 않는 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({'err_msg' : '서버 혹은 네트워크 오류로 이메일 전송을 실패했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([AllowAny])
def find_password_verify_code(request):
    if(request.method == 'POST'):
        try:
            verify_email = request.data['email']
            verify_code = request.data['verifyCode']
            cache_code = cache.get(verify_email)
            
            print(verify_email)
            print(verify_code)
            print(cache_code)
            
            # 인증 완료 후 캐시에서 삭제
            if(verify_code == cache_code):
                cache.delete(verify_email)
                # 인증 후 임시 비밀번호
                new_password = email_auth_string()
            
                send_mail(
                    'Sketch Day 임시 비밀번호입니다.',
                    recipient_list=[verify_email],
                    html=render_to_string('pwMailForm.html', {
                    'user_email': verify_email,
                    'auth_code': new_password,                   
                    })
                )    
            
                user = User.objects.get(auth_email=verify_email)
                user.set_password(new_password)
                user.save()
                
                return Response({'success':'success'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'err_msg':'잘못된 인증번호입니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
        except:
            return Response({'err_msg' : '임시 비밀번호 발급을 실패했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([IsAuthenticated])
def reset_password_verify(request):
    if(request.method == 'POST'):
        try:
            user = request.user
            curr_password = request.data['curr_password']
            user_id = user.user_id
            user = User.objects.get(user_id=user_id)
                
            if(user.check_password(curr_password)):
                return Response({'success' : '비밀번호 인증 성공'}, status=status.HTTP_200_OK)
                
            return Response({'err_msg':'비밀번호가 틀렸습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({'err_msg':'서버 오류로 인증을 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                
  


@ensure_csrf_cookie
@api_view(('POST',))
@permission_classes([IsAuthenticated])
def reset_password(request):
    if(request.method == 'POST'):
        try:
            user = request.user
            new_password = request.data['new_password']
            user_id = user.user_id
            user = User.objects.get(user_id=user_id)
            user.set_password(new_password)
            user.save()

            return Response({'success' : '비밀번호 변경 성공'}, status=status.HTTP_200_OK)
        
        except:
            return Response({'err_msg':'서버 오류로 인증을 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                
  


@ensure_csrf_cookie
@api_view(('DELETE',))
@permission_classes([IsAuthenticated])
def delete_user(request):
    if(request.method == 'DELETE'):
        try:
            user = request.user         
            user_id = user.user_id
            target_user = User.objects.get(user_id=user_id)
            target_user.delete()
                
            return Response({'success' : '회원탈퇴를 완료하였습니다.'}, status=status.HTTP_200_OK)
        
        except:
            return Response({'err_message':'회원탈퇴 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
