from abc import ABC, abstractmethod
from jose import jwt
from typing import Dict, List
from app.common.exceptions import UnauthorizedException
from datetime import datetime, timedelta 



class BaseAuth(ABC):

    @abstractmethod
    def jwt_decode_token(self, token) -> str:
        pass

    @abstractmethod
    def jwt_generate_token(self, token) -> Dict:
        pass

    # @abstractmethod
    # def check_auth(self, token: str, path: str, method: str) -> bool:
    #     pass
    

class ApiAuth(BaseAuth):

    def __init__(self, algorithms: List, private_key: str, expire_time: int = None) -> None:
        self.algorithms = algorithms
        self.private_key = private_key
        self.expire_time = expire_time

    def jwt_decode_token(self, token: str) -> str:
        """
        Decode bearer token.
        :param token:
        return decoded_token:
        """
        try:
            jwt_decoded = jwt.decode(
                token,
                self.private_key,
                algorithms=self.algorithms
            )
            return jwt_decoded
        except jwt.ExpiredSignatureError as e:
            raise UnauthorizedException("Token has expired.") from e
        except jwt.DecodeError as e:
            raise UnauthorizedException("Invalid token.") from e
    
    def jwt_generate_token(self, payload: object) -> str:
        """
        Generate a new JWT token.
        :param user_id: User ID or unique identifier
        :param expiration_minutes: Token expiration time in minutes
        :return: JWT token as a string
        """
        minutes= int(self.expire_time)
        payload['exp'] = datetime.utcnow() + timedelta(minutes)

        print(payload)
        jwt_token = jwt.encode(
                payload, 
                self.private_key, 
                algorithm=self.algorithms[0]
                )
        return jwt_token
  
      

    # Use an external API to check
    # def check_auth(self, token: str, path: str, method: str) -> bool:
    #     """
    #     Check if user is allowed to perform action in certain path.
    #     :param token: bearer token
    #     :param path: path to verify
    #     :param method: http method
    #     :return bool:
    #     """
    #     response = requests.post(
    #         f'{self.base_api_url}{self.check_auth_path}',
    #         json={'method': method, 'path': path},
    #         headers={'Authorization': f'Bearer {token}', 'accept': 'application/json'},
    #     ).json()
    #     if response.status_code == 200:
    #         return bool(response.json().get('isAllowed'))
    #     else:
    #         app.logger.warning("Failed to check auth: %d - %s", response.status_code, response.text)
    #         return False
