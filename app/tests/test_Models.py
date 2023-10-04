from app.models.studentsModel import Students
from app.models.resultModel import Results
from app.models.coursesModel import Courses
from app.models.usersModel import Users

from datetime import datetime


def test_student_model():
  
        student_data = {
            "first_name": "John",
            "family_name": "Doe",
            "date_birth": datetime(2000, 1, 1),
            "email_address": "john.doe@example.com",
            "dt_created": datetime(2023, 8, 24),
            "ic_active": True
        }

        student = Students(**student_data)
        student.to_dict()
        assert student.id_student is None # checking the key is present
        assert student.first_name == "John"
        assert student.family_name == "Doe"
        assert student.date_birth == datetime(2000, 1, 1)
        assert student.email_address == "john.doe@example.com"
        assert student.dt_created == datetime(2023, 8, 24)
        assert student.ic_active == True

def test_course_model():
  
        course_data = {
            "course_name": "Math",
            "dt_created": datetime(2023, 8, 24),
            "ic_active": True
        }

        courser = Courses(**course_data)
        courser.to_dict()
        assert courser.id_course is None # checking the key is present
        assert courser.course_name == "Math"
        assert courser.dt_created == datetime(2023, 8, 24)
        assert courser.ic_active == True


def test_result_model():
  
        result_data = {
            "cd_student": 1,
            "cd_course": 1,
            "score": "A",
            "dt_created": datetime(2023, 8, 24),
            "ic_active": True
        }



        result = Results(**result_data)
        result.to_dict()
        assert result.id_result is None # checking the key is present
        assert result.cd_student == 1
        assert result.cd_course == 1
        assert result.score == "A"
        assert result.dt_created == datetime(2023, 8, 24)
        assert result.ic_active == True
      

def test_user_model():
  
        user_data = {
            "st_firstname": "John",
            "st_lastname": "Doe",
            "username": "Admin",
            "em_user_email": "john.doe@example.com",
            "password": "123456789",
            "dt_created": datetime(2023, 8, 24),
            "ic_active": True
        }


        user = Users(**user_data)
        user.to_dict()
        assert user.id_user is None # checking the key is present
        assert user.st_firstname == "John"
        assert user.st_lastname == "Doe"
        assert user.username == "Admin"
        assert user.em_user_email == "john.doe@example.com"
        assert user.password == "123456789"
        assert user.dt_created == datetime(2023, 8, 24)
        assert user.ic_active == True
      
