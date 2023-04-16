from django.http import HttpRequest, HttpResponseNotFound

# Error 처리 view (DEBUG = False일 경우만 동작)
def error_404_view(request, exception):
    return HttpResponseNotFound("The page is not found")