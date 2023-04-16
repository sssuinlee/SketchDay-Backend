from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def diary_write(request, username):
    return HttpResponse("Hi %s :) How's going today? Write your day" % username)

def diary_read(request, title):
    return HttpResponse("Your Diary: %s" % title)

# HttpResponseRedirect('new_url')
def redirect_test(request):
    return HttpResponseRedirect('write/username')