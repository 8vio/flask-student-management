import json
from unittest.mock import patch, MagicMock  
from contextlib import contextmanager
from app.models.studentsModel import Students
from app.common.security.providers import BaseAuth
from app.common.security.jwtService import JWTBearer
from app import db
from datetime import datetime
from app.common.custom_encoder import CustomEncoder
from werkzeug.exceptions import Unauthorized
from dataclasses import dataclass

@dataclass
class MockStudent:
    id_student: int
    first_name: str
    family_name: str
    date_birth: datetime
    email_address: str
    dt_created: datetime
    ic_active: bool

class MockStudentsSchema:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def create_mock_schema(mock_students_data):
        return {
            "students": mock_students_data
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
def common_setup(mock_student_id=None):
    with patch("app.common.security.jwtService.JWTBearer", new=MockJWTBearer):
        mock_students = patch("app.models.studentsModel.Students").start()

        mock_students_schema_instance = MockStudentsSchema()

        with patch("app.schemas.studentsSchema.StudentsSchema", return_value=mock_students_schema_instance):
            with patch.object(db, "session") as mock_session, \
                 patch.object(mock_session, "begin") as mock_begin, \
                 patch.object(mock_session, "commit"):
                if mock_student_id is not None:
                    mock_get_by_id = MagicMock()
                    mock_students.get_by_id.return_value = {
                        "id_student": mock_student_id,
                        "first_name": "John",
                        "family_name": "Doe",
                        "date_birth": datetime(2000, 1, 1),
                        "email_address": "john.doe@example.com",
                        "dt_created": datetime(2023, 8, 24),
                        "ic_active": True
                    }
                    mock_students.get_by_id = mock_get_by_id

                yield mock_students

        mock_students.stop()

## MagicMock itself is not None (No working in view with "Empty MagickMock")
@contextmanager
def common_setup_no_students():
    with patch("app.common.security.jwtService.JWTBearer", new=MockJWTBearer):
        yield None



### Happy Path
def test_create_student(client):
    with common_setup() as mock_students, \
         patch.object(db.session, "add", return_value=None), \
         patch.object(db.session, "commit", return_value=None):
        student_data = {
            "first_name": "John",
            "family_name": "Doe",
            "date_birth": "2000-01-01",
            "email_address": "john.doe@example.com"
        }
        response = client.post(
            "/students",
            json=student_data,
            headers={"Authorization": "Bearer mocked_token"}
        )
        if response.status_code == 500:
            print(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert "id_student" in response.json


def test_get_students(client):
    mock_students_data = [
        {
            "first_name": "John",
            "family_name": "Doe",
            "date_birth": datetime(2000, 1, 1), 
            "email_address": "john.doe@example.com",
            "dt_created": datetime(2023, 8, 24)  
        }
    ]

    with common_setup() as mock_students, \
        patch("app.views.studentsView.StudentsSchema") as mock_students_schema:
        mock_students_schema.return_value.dict.return_value = {"students": mock_students_data}

        response = client.get("/students", headers={"Authorization": "Bearer mocked_token"})
        assert response.status_code == 200

def test_get_student_by_id(client):
    with common_setup(mock_student_id=1) as mock_students:
        mock_students.get_by_id.return_value = MockStudent(
            id_student=1,
            first_name="John",
            family_name="Doe",
            date_birth=datetime(2000, 1, 1),
            email_address="john.doe@example.com",
            dt_created=datetime(2023, 8, 24),
            ic_active=True
        )

        response = client.get("/students/1", headers={"Authorization": "Bearer mocked_token"})
        assert response.status_code == 200


def test_patch_student(client):
    with common_setup(mock_student_id=1) as mock_students, \
         patch.object(db.session, "commit", return_value=None):
        update_data = {
            "first_name": "Jane",
            "family_name": "Smith"
        }

        mock_students.get_by_id.return_value = {
                        "id_student": 1,
                        "first_name": "John",
                        "family_name": "Doe",
                        "date_birth": datetime(2000, 1, 1),
                        "email_address": "john.doe@example.com",
                        "dt_created": datetime(2023, 8, 24),
                        "ic_active": True
                    }

        response = client.patch(
            "/students/1",
            json=update_data,
            headers={"Authorization": "Bearer mocked_token"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Student updated successfully"
       

def test_delete_student(client):
    with common_setup(mock_student_id=1) as mock_students, \
         patch.object(db.session, "commit", return_value=None):

        response = client.delete(
            "/students/1",
            headers={"Authorization": "Bearer mocked_token"}
        )
        assert response.status_code == 204


## Failure 


## 401 Tests
def test_unauthorized(client):
    with common_setup(), \
         patch.object(MockJWTBearer, "_verify_jwt", side_effect=Unauthorized("Unauthorized")):
        response = client.get("/students", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401


## 404 Tests

def test_get_student_by_id_not_found(client):
    with common_setup_no_students():
        response = client.get("/students/1", headers={"Authorization": "Bearer mocked_token"})
        assert response.status_code == 404


def test_patch_student_by_id_not_found(client):
    with common_setup_no_students():
        update_data = {
            "first_name": "Jane",
            "family_name": "Smith"
        }

        response = client.patch(
            "/students/1",
            json=update_data,
            headers={"Authorization": "Bearer mocked_token"}
        )
        assert response.status_code == 404

        
def test_delete_student_by_id_not_found(client):
    with common_setup_no_students():
        response = client.delete(
            "/students/1",
            headers={"Authorization": "Bearer mocked_token"}
        )
        assert response.status_code == 404

