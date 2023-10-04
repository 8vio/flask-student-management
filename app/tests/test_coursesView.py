import json
from unittest.mock import patch, MagicMock  
from contextlib import contextmanager
from app.models.coursesModel import Courses
from app.common.security.providers import BaseAuth
from app.common.security.jwtService import JWTBearer
from app import db
from datetime import datetime
from app.common.custom_encoder import CustomEncoder
from werkzeug.exceptions import Unauthorized
from dataclasses import dataclass

@dataclass
class MockCourse:
    id_course: int
    course_name: str
    dt_created: datetime
    ic_active: bool

class MockCoursesSchema:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def create_mock_schema(mock_courses_data):
        return {
            "courses": mock_courses_data
        }

    
class MockSession:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def query(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return []

class MockJWTBearer(JWTBearer):
    def __init__(self, auth_provider: BaseAuth):
        super().__init__(auth_provider)
    
    def _verify_jwt(self, token: str) -> dict:
        return {"id_user": "mocked_id"}


@contextmanager
def common_setup(mock_course_id=None):
    with patch("app.common.security.jwtService.JWTBearer", new=MockJWTBearer):
        mock_courses = patch("app.models.coursesModel.Courses").start()

        mock_courses_schema_instance = MockCoursesSchema()

        with patch("app.schemas.coursesSchema.CoursesSchema", return_value=mock_courses_schema_instance):
            with patch.object(db, "session") as mock_session, \
                 patch.object(mock_session, "begin") as mock_begin, \
                 patch.object(mock_session, "commit"):
                if mock_course_id is not None:
                    mock_get_by_id = MagicMock()
                    mock_courses.get_by_id.return_value = {
                        "id_course": mock_course_id,
                        "course_name": "Math",
                        "dt_created": datetime(2023, 8, 24),
                        "ic_active": True
                    }
                    mock_courses.get_by_id = mock_get_by_id

                yield mock_courses

        mock_courses.stop()

## MagicMock itself is not None (No working in view with "Empty MagickMock")
@contextmanager
def common_setup_no_courses():
    with patch("app.common.security.jwtService.JWTBearer", new=MockJWTBearer):
        yield None



### Happy Path
def test_create_student(client):
    with common_setup() as mock_courses, \
         patch.object(db.session, "add", return_value=None), \
         patch.object(db.session, "commit", return_value=None):
        student_data = {
            "course_name": "Math",
        }
        response = client.post(
            "/courses",
            json=student_data,
            headers={"Authorization": "Bearer mocked_token"}
        )
        if response.status_code == 500:
            print(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert "id_course" in response.json


def test_get_courses(client):
    mock_courses_data = [
        {
            "course_name": "Math",
            "dt_created": datetime(2023, 8, 24)  
        }
    ]

    with common_setup() as mock_courses, \
        patch("app.views.coursesView.CoursesSchema") as mock_courses_schema:
        mock_courses_schema.return_value.dict.return_value = {"courses": mock_courses_data}

        response = client.get("/courses", headers={"Authorization": "Bearer mocked_token"})
        assert response.status_code == 200

def test_get_student_by_id(client):
    with common_setup(mock_course_id=1) as mock_courses:
        mock_courses.get_by_id.return_value = MockCourse(
            id_course=1,
            course_name="Math",
            dt_created=datetime(2023, 8, 24),
            ic_active=True
        )

        response = client.get("/courses/1", headers={"Authorization": "Bearer mocked_token"})
        assert response.status_code == 200


def test_patch_student(client):
    with common_setup(mock_course_id=1) as mock_courses, \
         patch.object(db.session, "commit", return_value=None):
        update_data = {
            "course_name": "Retail"
        }

        mock_courses.get_by_id.return_value = {
                        "id_course": 1,
                        "course_name": "Math",
                        "dt_created": datetime(2023, 8, 24),
                        "ic_active": True
                    }

        response = client.patch(
            "/courses/1",
            json=update_data,
            headers={"Authorization": "Bearer mocked_token"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Course updated successfully"
       

def test_delete_student(client):
    with common_setup(mock_course_id=1) as mock_courses, \
         patch.object(db.session, "commit", return_value=None):

        response = client.delete(
            "/courses/1",
            headers={"Authorization": "Bearer mocked_token"}
        )
        assert response.status_code == 204


## Failure 


## 401 Tests
def test_unauthorized(client):
    with common_setup(), \
         patch.object(MockJWTBearer, "_verify_jwt", side_effect=Unauthorized("Unauthorized")):
        response = client.get("/courses", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401


## 404 Tests

def test_get_student_by_id_not_found(client):
    with common_setup_no_courses():
        response = client.get("/courses/1", headers={"Authorization": "Bearer mocked_token"})
        assert response.status_code == 404


def test_patch_student_by_id_not_found(client):
    with common_setup_no_courses():
        update_data = {
            "course_name": "Jane",
            "family_name": "Smith"
        }

        response = client.patch(
            "/courses/1",
            json=update_data,
            headers={"Authorization": "Bearer mocked_token"}
        )
        assert response.status_code == 404

        
def test_delete_student_by_id_not_found(client):
    with common_setup_no_courses():
        response = client.delete(
            "/courses/1",
            headers={"Authorization": "Bearer mocked_token"}
        )
        assert response.status_code == 404

