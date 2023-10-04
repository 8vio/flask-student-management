from functools import wraps
from app.common.security.providers import BaseAuth
from app.common.exceptions import UnauthorizedException
from flask import request 

class JWTBearer:

    def __init__(self, auth_provider: BaseAuth):
        self.__auth_provider = auth_provider

    def __call__(self, *args, **kwargs) -> str:
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header is None:
                raise UnauthorizedException('Authorization header missing.')
            if authorization_header.startswith('Bearer '):
                token = authorization_header.split(" ")[1]
            else:
                token = authorization_header
        except Exception as e:
            raise UnauthorizedException('Bearer token not found.') from e
        decoded_token = self._verify_jwt(token)
        # Add access control 
        # is_allowed = self._check_auth(decoded_token, request.path, request.method)
        # if not is_allowed:
        #     raise ForbiddenException("Insufficient permissions.")
        return decoded_token

    def _verify_jwt(self, token: str) -> str:
        """
        Return decoded token if valid.
        :param token:
        :return decoded_token:
        """
        try:
            return self.__auth_provider.jwt_decode_token(token)
        except Exception as e:
            raise UnauthorizedException("Invalid token.", e) from e

    def generate_token(self, id_user: str) -> str:
        """
        Generate a new JWT token.
        :param id_user: User ID or unique identifier
        :return: JWT token as a string
        """
        try:
            payload = {
                    'id_user': id_user
            }
            print(payload)
            return self.__auth_provider.jwt_generate_token(payload)
        except Exception as e:
            raise UnauthorizedException("Error generating token.") from e



def jwt_required(f, auth_prodiver):
    """
    Checks whether JWT bearer is valid and if it has access for an specific
    path.
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        JWTBearer(auth_prodiver)()
        return f(*args, **kwargs)
    return decorator
