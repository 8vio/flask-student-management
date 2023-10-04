import json
from flask import current_app as app
from flask import request, jsonify, abort
from flask.views import MethodView
from app.common.exceptions import ObjectNotFoundException
from app.models.usersModel import Users
from app.schemas.usersSchema import UserCreationSchema, UsersSchema
from flask_bcrypt import generate_password_hash
from flask_restx import Namespace, fields 

# Create a namespace for the user view
user_ns = Namespace('users', description='User operations')
# Define the model for the request body using fields
user_model = user_ns.model('UserModel', {
    'st_firstname': fields.String(required=True, description='User First Name'),
    'st_lastname': fields.String(required=True, description='User Lastname'),
    'username': fields.String(required=True, description='Username'),
    'em_user_email': fields.String(required=True, description='User Email'),
    'password': fields.String(required=True, description='User Password')
})


class UsersView(MethodView):
    @staticmethod
    @user_ns.expect(user_model, validate=True)
    def post():
        try:

            data = json.loads(UserCreationSchema(**request.get_json()).json())
            pw_hash = generate_password_hash(data['password'], 10).decode('utf-8')
            data["password"] = pw_hash
            user = Users(
                **data
            )
            user.save()
            return {"id_user":user.id_user}, 200
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    @user_ns.doc(security="Bearer")
    def get():
        try:
            schema = UsersSchema(users=Users.simple_filter(ic_active=True))
            result = schema.dict()  
            # Format dt_created for all users
            for user_dict in result['users']:
                user_dict['dt_created'] = user_dict['dt_created'].strftime("%m/%d/%Y")  
            return result, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)

@user_ns.doc(security="Bearer")   
class UsersViewbyId(MethodView):
   
    @staticmethod
    def get(id):
        try:
            user = Users.get_by_id(id)
            if not user:
                raise ObjectNotFoundException("User not found")
            result = user.to_dict()
            return result, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)

    @staticmethod
    def patch(id):
        try:
            data = request.get_json()
            user = Users.get_by_id(id)
           
            if not user:
                raise ObjectNotFoundException("User not found")
            
            for key, value in data.items():
                setattr(user, key, value)
            
            user.save()
            return {"message": "User updated successfully"}, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def delete(id):
        try:
            user = Users.get_by_id(id)
            if not user:
                raise ObjectNotFoundException("User not found")
            user.ic_active = False
            user.save()
            return {"message": "User Deleted successfully"}, 204
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


user_ns.add_resource(UsersView, '')
user_ns.add_resource(UsersViewbyId, '/<id>')