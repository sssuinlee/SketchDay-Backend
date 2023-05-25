import string
import random
import threading
import jwt
from backend.config.settings.base import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .serializers import BaseUserSerializer
from backend.config.settings.base import SECRET_KEY


# 제목, 메세지, 송신자, 수신자 리스트, fail_silently(false인 경우 메일 발송에 실패했을 때 알림), html
class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, recipient_list,
              fail_silently, html):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)
    
    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.message, self.from_email, to=self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)


# user의 이메일로 인증코드를 발송해주는 역할 수행
def send_mail(subject, recipient_list, message='', 
              from_email=EMAIL_HOST_USER,
              fail_silently=False, html=None, *args, **kwargs):
    EmailThread(
        subject, message, from_email, recipient_list, fail_silently, html
        ).start()


# 인증 번호를 랜덤으로 생성해주는 함수
def email_auth_string():
    LENGTH = 12
    string_pool = string.ascii_letters + string.digits
    auth_string = ""
    
    for i in range(LENGTH):
        auth_string += random.choice(string_pool)
    
    return auth_string 


def user_authenticate(cookies):
    try:
        access_token = cookies['access_token']
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        auth_email = payload['user_id']
        user = User.objects.get(auth_email=auth_email)
        serializer = BaseUserSerializer(user)
        user_data = serializer.data
        return (True, user_data)
    
    # access token 만료
    except jwt.exceptions.ExpiredSignatureError:
        data = {'refresh': cookies.get('refresh_token', None)}
        serializer = TokenRefreshSerializer(data=data)
        
        try:
            if serializer.is_valid(raise_exception=True):
                access_token = serializer.validated_data['access']
                refresh_token = cookies.get('refresh_token', None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
                auth_email = payload['user_id']
                user = User.objects.get(auth_email=auth_email)
                serializer = BaseUserSerializer(user)
                user_data = serializer.data
                return (True, user_data, access_token, refresh_token)
            
        # refresh token 만료 = 로그인 만료
        except TokenError:
            return (False, '로그인이 만료되었습니다.')
    
    # 위조되거나 잘못됨
    except jwt.exceptions.InvalidTokenError:
        return (False,)

    # 토큰이 없음 = 로그인 상태가 아님
    except KeyError:
        return (False,)
  

def is_logged_in(cookies):
    access_token = cookies.get('access_token', None)
    if(access_token is None):
        return False
    return True