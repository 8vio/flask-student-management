import json
from flask import current_app as app
from flask import request, jsonify, abort
from flask.views import MethodView
from app.common.exceptions import ObjectNotFoundException
from app.models.resultModel import Results
from app.models.studentsModel import Students
from app.models.coursesModel import Courses
from app.schemas.resultSchema import ResultsCreationSchema
from flask_restx import Namespace, fields 
from app import db

# Create a namespace for the rrsult view
result_ns = Namespace('results', description='Results operations')
# Define the model for the request body using fields
result_model = result_ns.model('ResultModel', {
    'cd_student': fields.Integer(required=True, description='Id Student'),
    'cd_course': fields.Integer(required=True, description='Id Course'),
    'score': fields.String(required=True, description='Score'),

})

@result_ns.doc(security="Bearer")
class ResultsView(MethodView):
    @staticmethod
    @result_ns.expect(result_model, validate=True)
    def post():
        try:
            data = json.loads(ResultsCreationSchema(**request.get_json()).json())
            result = Results(
                **data
            )
            result.save()
            return {"id_result":result.id_result}, 200
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def get():
        try:

            results_list = (
            db.session.query(
                Results.id_result,
                Students.first_name + ' ' + Students.family_name,
                Courses.course_name,
                Results.score
            )
            .join(Courses, Courses.id_course == Results.cd_course)
            .join(Students, Students.id_student == Results.cd_student)
            .filter(Results.ic_active == True)
            .filter(Students.ic_active == True)
            .filter(Courses.ic_active == True)
            .all()
            )
            
            formatted_results = []
            for result in results_list:
                id_result, student_name, course_name, score = result
                formatted_results.append({
                    "id_result": id_result,
                    "student": student_name,
                    "course": course_name,
                    "score": score
                })

            return formatted_results, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)

@result_ns.doc(security="Bearer")
class ResultsViewbyId(MethodView):

    @staticmethod
    def get(id):
        try:
            result_student = Results.get_by_id(id)
            if not result_student:
                raise ObjectNotFoundException("User not found")
            result = result_student.to_dict()
            return result, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)

    @staticmethod
    @result_ns.expect(result_model, validate=True)
    def patch(id):
        try:
            data = request.get_json()
            result = Results.get_by_id(id)
           
            if not result:
                raise ObjectNotFoundException("Result not found")
            
            for key, value in data.items():
                setattr(result, key, value)
            
            result.save()
            return {"message": "Result updated successfully"}, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def delete(id):
        try:
            result = Results.get_by_id(id)
            if not result:
                raise ObjectNotFoundException("Result not found")
            result.ic_active = False
            result.save()
            return {"message": "Result Deleted successfully"}, 204
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


result_ns.add_resource(ResultsView, '')
result_ns.add_resource(ResultsViewbyId, '/<id>')