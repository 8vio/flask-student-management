from .coursesView import CoursesView, CoursesViewbyId
from .loginView import LoginView, login_ns
from .resultsView import ResultsView, ResultsViewbyId, result_ns
from .studentsView import StudentsView, StudentsViewbyId, student_ns
from .usersView import UsersView, UsersViewbyId, user_ns
from .coursesView import CoursesView, CoursesViewbyId, course_ns
__all__ = [
    "CoursesView",
    "CoursesViewbyId",
    "LoginView",
    "ResultsView",
    "ResultsViewbyId",
    "StudentsView",
    "StudentsViewbyId",
    "UsersView",
    "UsersViewbyId"
]

__namespaces__ = [
    login_ns,
    result_ns,
    student_ns,
    user_ns,
    course_ns
]
