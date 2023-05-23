from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login_view'),
    # path('login', views.UserLoginAPI.as_view(), name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('signup', views.signup_view, name='signup_view'),
    path('sendEmail', views.send_verification_code, name='send_verification_code'),
    path('verifyEmail', views.verify_code, name='verify_code')
]
