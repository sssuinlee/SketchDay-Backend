from rest_framework.response import Response
from rest_framework import status
from account.models import User
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view
from account.serializers import UserInfoSerializer
from django.db.models import functions


# @ensure_csrf_cookie
@csrf_exempt
@api_view(('GET',))
def mypage_view(request):
    if (request.method == 'GET'):
        if(request.user.is_authenticated):
            user_id = request.user.user_id
            res_data_raw = User.objects.values('name', 'auth_email', 'birth') \
                .get(user_id = user_id)
            serializer = UserInfoSerializer(res_data_raw)
            res_data_json = serializer.data
            return Response({'message' : '조회에 성공하였습니다.', 'data' : res_data_json}, status=status.HTTP_200_OK)
        else:
            return Response({'err_msg' : '잘못된 접근입니다.'}, status=status.HTTP_403_FORBIDDEN)

