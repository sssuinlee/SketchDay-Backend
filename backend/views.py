from django.http import HttpResponseNotFound
from django.shortcuts import render

# Error 처리 view (DEBUG = False일 경우만 동작)
def error_404_view(request, exception):
    return HttpResponseNotFound("The page is not found")

def index(request):
    return render(request, 'main.html')