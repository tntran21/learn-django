import jwt
from django.conf import settings


class AccountUtils:
    @staticmethod
    def generate_jwt_token(user):
        payload = {
            "email": user["email"],
        }

        token = jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def decode_jwt_token(token):
        try:
            payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms="HS256")
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
