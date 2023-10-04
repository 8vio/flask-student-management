from flask import current_app as app
from flask import request, abort
from flask.views import MethodView
from app.common.exceptions import UnauthorizedException
from app.models.usersModel import Users
from app.schemas.loginSchema import LoginSchema 
from app.common.security import JWTBearer, ApiAuth
import os
from flask_bcrypt import check_password_hash
from flask_restx import Namespace, fields 

# Create a namespace for the login view
login_ns = Namespace('login', description='Login operations')
# Define the model for the request body using fields
login_model = login_ns.model('LoginModel', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

auth_provider = ApiAuth(
    ["HS256"],
    os.environ.get('SECRET_KEY'),
    os.environ.get('TOKEN_EXPIRES')
    
)

class LoginView(MethodView):
    
    
    @staticmethod
    @login_ns.expect(login_model, validate=True)
    def post():
        try:   
            data = LoginSchema(**request.get_json())
            user = Users.simple_filter(username=data.username)[0]

            #Validate password
            if user and check_password_hash(user.password, data.password):
                # Password is correct, generate token
                generateToken  = JWTBearer(auth_provider)
                token = generateToken.generate_token(user.id_user)
                return {"token":token}, 200
            else:
                raise UnauthorizedException("Invalid credentials")
        except UnauthorizedException as e:
            abort(401, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)



login_ns.add_resource(LoginView, '')
