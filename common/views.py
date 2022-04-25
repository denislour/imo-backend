from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
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


class LoginAPIView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        return Response(UserSerializer(user).data)
