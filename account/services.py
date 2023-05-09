import string
import random
import threading
from backend.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives


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