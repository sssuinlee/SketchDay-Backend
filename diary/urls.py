from django.urls import path
from . import views

urlpatterns = [
    path('write/<slug:username>', views.diary_write),
    path('read/<title>', views.diary_read),
    path('redirect', views.redirect_test)
]