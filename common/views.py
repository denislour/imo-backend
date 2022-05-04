from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from .authen import JWTAuthentication
from .serializers import UserSerializer


class RegisterAPIView(APIView):

    def post(self, request):
        data = request.data
        if data.get('password') != data.get('password_confirm'):
            return APIException('Password does not match!!!')
        data['is_ambassador'] = 'api/ambassador' in request.path
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

        scope = 'ambassador' if 'api/ambassador' in request.path else 'admin'

        if user.is_ambassador and scope == 'admin':
            raise AuthenticationFailed('Unauthorized!')

        token = JWTAuthentication.generate_jwt(user.id, scope)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'message': 'success'}
        return response


class UserAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UsersAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, _):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'success'
        }
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data.get('password') != data.get('password_confirm'):
            raise APIException('Password do not match!')
        user.set_password(data.get('password'))
        user.save()
        return Response(UserSerializer(user).data)
