from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Error 처리 view (DEBUG = False일 경우만 동작)
def error_404_view(request, exception):
    return HttpResponseNotFound("The page is not found")

def index(request):
    return render(request, 'main.html')