from django.shortcuts import render, redirect
from s3_storage.models import Image

# Create your views here.
def test(request):
    return render(request, 'index.html')

def show_img(request):
    if request.method == 'POST':
        img = request.FILES.get('img-file')
        Image.objects.create(img=img)
        return redirect(show_img)
    else:
        img = Image.objects.first()
    context = {
        'object': img
    }
    return render(request, 'index.html', context)
