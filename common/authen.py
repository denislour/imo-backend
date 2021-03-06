import jwt
import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from app import settings
from core.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        is_ambassador = 'api/ambassador' in request.path
        token = request.COOKIES.get('jwt')
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.get(pk=payload.get('user_id'))

        if user is None:
            raise AuthenticationFailed('User not found!')

        if is_ambassador and payload.get('scope') != 'ambassador' or (
                not is_ambassador and payload.get('scope') != 'admin'):
            raise AuthenticationFailed('Invalid Scope!')

        return user, None

    @staticmethod
    def generate_jwt(user_id, scope):
        payload = {
            'user_id': user_id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, key=settings.SECRET_KEY, algorithm='HS256')
