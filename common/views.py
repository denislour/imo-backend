from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegisterAPIView(APIView):

    def post(self, request):
        data = request.data
        if data.get('password') != data.get('password_confirm'):
            return APIException('Password does not match!!!')
        data['is_ambassador'] = 0
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
