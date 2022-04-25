import jwt, datetime
from app import settings


class JWTAuthentication():

    @staticmethod
    def generate_jwt(user_id):
        payload = {
            'admin_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, key=settings.SECRET_KEY, algorithm='HS256')
