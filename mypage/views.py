from rest_framework.response import Response
from rest_framework import status
from account.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from account.serializers import UserInfoSerializer


@ensure_csrf_cookie
@api_view(('GET',))
def mypage_view(request):
    if (request.method == 'GET'):
        try:
            user = request.user
            user_id = user.user_id
            res_data_raw = User.objects.values('name', 'auth_email', 'birth') \
                .get(user_id = user_id)
            serializer = UserInfoSerializer(res_data_raw)
            res_data_json = serializer.data
            
            return Response({'message' : '조회에 성공하였습니다.', 'data' : res_data_json}, status=status.HTTP_200_OK)
        
        except:
            return Response({'err_msg' : '서버 오류로 조회에 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

