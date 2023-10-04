import json
from flask import current_app as app
from flask import request, jsonify, abort
from flask.views import MethodView
from app.common.exceptions import ObjectNotFoundException
from app.models.coursesModel import Courses
from app.schemas.coursesSchema import CoursesCreationSchema, CoursesSchema
from flask_restx import Namespace, fields 

# Create a namespace for the course view
course_ns = Namespace('courses', description='Courses operations')
# Define the model for the request body using fields
course_model = course_ns.model('CourseModel', {
    'course_name': fields.String(required=True, description='Course Name')

})


@course_ns.doc(security="Bearer")
class CoursesView(MethodView):
    @staticmethod
    @course_ns.expect(course_model, validate=True)
    def post():
        try:
            data = json.loads(CoursesCreationSchema(**request.get_json()).json())
            course = Courses(
                **data
            )
            course.save()
            return {"id_course":course.id_course}, 200
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def get():
        try:
            schema = CoursesSchema(courses=Courses.simple_filter(ic_active=True))
            course = schema.dict()  
            # Format dt_created for all results
            for course_dict in course['courses']:
                course_dict['dt_created'] = course_dict['dt_created'].strftime("%m/%d/%Y")  
            return course['courses'], 200
        except Exception as e:
            app.logger.exception(e)
            abort(500)

@course_ns.doc(security="Bearer")
class CoursesViewbyId(MethodView):
   
    @staticmethod
    def get(id):
        try:
            course = Courses.get_by_id(id)
            if not course:
                raise ObjectNotFoundException("Course not found")
            result = course.to_dict()
            return result, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)

    @staticmethod
    @course_ns.expect(course_model, validate=True)
    def patch(id):
        try:
            data = request.get_json()
            course = Courses.get_by_id(id)
           
            if not course:
                raise ObjectNotFoundException("Course not found")
            
            for key, value in data.items():
                setattr(course, key, value)
            
            course.save()
            return {"message": "Course updated successfully"}, 200
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)


    @staticmethod
    def delete(id):
        try:
            course = Courses.get_by_id(id)
            if not course:
                raise ObjectNotFoundException("Course not found")
            course.ic_active = False
            course.save()
            return {"message": "Course Deleted successfully"}, 204
        except ObjectNotFoundException as e:
            abort(404, description=str(e))
        except Exception as e:
            app.logger.exception(e)
            abort(500)

course_ns.add_resource(CoursesView, '')
course_ns.add_resource(CoursesViewbyId, '/<id>')