from django.urls import path
from . import views

urlpatterns = [
    path('userInfo', views.mypage_view, name='mypage_view'),
]