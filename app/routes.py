"""
DESC: Collection of routes for your views with its IDP.
USAGE:
view_rules = [
    Rule(
        path='/path/to/endpoint/',
        view=view_func or ClassView.as_view(),
        auth_provider=auth_provider
    )
}]
"""
import os
from collections import namedtuple
from app.common.security import ApiAuth
from app.views.usersView import UsersView, UsersViewbyId
from app.views.studentsView import StudentsView, StudentsViewbyId
from app.views.coursesView import CoursesView, CoursesViewbyId
from app.views.resultsView import ResultsView, ResultsViewbyId
from app.views.loginView import LoginView



Rule = namedtuple('Rule', ['path', 'view', 'auth_provider', 'methods'])
RuleNonAuth = namedtuple('Rule', ['path', 'view', 'methods'])

auth_provider = ApiAuth(
    ["HS256"],
    os.environ.get('SECRET_KEY')
)

view_rules = [

     Rule( 
        path = '/users',
        view = UsersView.as_view('get-users'),
        auth_provider=auth_provider,
        methods=['GET']
    ),

    Rule( 
        path = '/users/<id>',
        view = UsersViewbyId.as_view('manage-user'),
        auth_provider=auth_provider,
        methods=['PATCH','DELETE','GET']
    ),

    Rule( 
        path = '/students/<id>',
        view = StudentsViewbyId.as_view('manage-student'),
        auth_provider=auth_provider,
        methods=['PATCH','DELETE','GET']
    ),
    
     Rule( 
        path = '/students',
        view = StudentsView.as_view('create-student'),
        auth_provider=auth_provider,
        methods=['POST','GET']
    ),

     Rule( 
        path = '/courses',
        view = CoursesView.as_view('create-courses'),
        auth_provider=auth_provider,
        methods=['POST','GET']
    ),

    Rule( 
        path = '/courses/<id>',
        view = CoursesViewbyId.as_view('manage-courses'),
        auth_provider=auth_provider,
        methods=['PATCH','DELETE','GET']
    ),
      Rule( 
        path = '/results',
        view = ResultsView.as_view('create-results'),
        auth_provider=auth_provider,
        methods=['POST','GET']
    ),

    Rule( 
        path = '/results/<id>',
        view = ResultsViewbyId.as_view('manage-results'),
        auth_provider=auth_provider,
        methods=['PATCH','DELETE','GET']
    )

]


view_rules_nonauth = [


    RuleNonAuth( 
        path = '/users',
        view = UsersView.as_view('create-user'),
        methods=['POST']
    ),

 
    RuleNonAuth( 
        path = '/login',
        view = LoginView.as_view('login'),
        methods=['POST']
    )

]
