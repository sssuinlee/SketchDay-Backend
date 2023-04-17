from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView ,DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .analyzer import generate_image
from .serializers import DiaryImageSerializer
from .models import DiaryImg

class GenerateImage(CreateAPIView):
    model = DiaryImg
    serializer_class = DiaryImageSerializer
    def perform_create(self, serializer):
        if serializer.is_vaild():
            prompt = self.request.data.get("prompt", None)
            generated_img = generate_image(prompt)
            serializer.save(
                generated_img
            )
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_REQUEST)

class UpdatePostView(UpdateAPIView) :
    queryset = DiaryImg.objects.all()
    serializer_class = DiaryImageSerializer
    lookup_field = 'pk'

class DeletePostView(DestroyAPIView):
    queryset = DiaryImg.objects.all()
    serializer_class = DiaryImageSerializer
    lookup_field = 'pk'