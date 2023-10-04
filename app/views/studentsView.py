import json
from flask import current_app as app
from flask import request, jsonify, abort
from flask.views import MethodView
from app.common.exceptions import ObjectNotFoundException
from app.models.studentsModel import Students
from app.schemas.studentsSchema import StudentCreationSchema, StudentsSchema
from flask_restx import Namespace, fields 
from datetime import datetime


# Create a namespace for the login view
student_ns = Namespace('students', description='Students operations')
# Define the model for the request body using fields
student_model = student_ns.model('StudentModel', {
    'first_name': fields.String(required=True, description='First Name'),
    'family_name': fields.String(required=True, description='Family Name'),
    'date_birth': fields.String(required=True, description='Date of Birth'),
    'email_address': fields.String(required=True, description='Email Address')
})


@student_ns.doc(security="Bearer")
class StudentsView(MethodView):
    @staticmethod
    @student_ns.expect(student_model, validate=True)
    def post():
        try:
            data = json.loads(StudentCreationSchema(**request.get_json()).json())
            print(data["date_birth"])
            data["date_birth"] = datetime.strptime(data["date_birth"], '%Y-%m-%d')
            student = Students(
                **data
            )
            student.save()
            return {"id_student":student.id_student}, 200
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def get():
        try:
            schema = StudentsSchema(students=Students.simple_filter(ic_active=True))
            result = schema.dict()  
            # Format dt_created for all students
            for student_dict in result['students']:
                student_dict['dt_created'] = student_dict['dt_created'].strftime("%m/%d/%Y")
                student_dict['date_birth'] = student_dict['date_birth'].strftime("%m/%d/%Y")  
            return result['students'], 200
        except Exception as e:
            app.logger.exception(e)
            abort(500)

            

@student_ns.doc(security="Bearer")
class StudentsViewbyId(MethodView):

    @staticmethod
    def get(id):
        try:
            student = Students.get_by_id(id)
            print("Returned student:", student)
            if not student:
                raise ObjectNotFoundException("User not found")
            result = student.to_dict()
            # return result, 200
            return result, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e: 
            app.logger.exception(e)
            abort(500)

    @staticmethod
    @student_ns.expect(student_model, validate=True)
    def patch(id):
        try:
            data = request.get_json()
            student = Students.get_by_id(id)
           
            if not student:
                raise ObjectNotFoundException("Student not found")
            
            for key, value in data.items():
                setattr(student, key, value)
            
            student.save()
            return {"message": "Student updated successfully"}, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def delete(id):
        try:
            student = Students.get_by_id(id)
            if not student:
                raise ObjectNotFoundException("Student not found")
            student.ic_active = False
            student.save()
            return {"message": "Student Deleted successfully"}, 204
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


student_ns.add_resource(StudentsView, '')
student_ns.add_resource(StudentsViewbyId, '/<id>')