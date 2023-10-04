from flask import Flask, jsonify, render_template, redirect
from flask_cors import CORS

from app.db import db
from app.ext import migrate
from app.common.exceptions import (
    BadRequestException, ForbiddenException, InternalServerErrorException, ObjectNotFoundException,
    UnauthorizedException
)

from app.common.exceptions.http_exceptions import ObjectNotFoundException
from app.common.security import jwt_required
from app.routes import view_rules, view_rules_nonauth
from flask_bcrypt import Bcrypt
from flask_restx import Api


from app.models.usersModel import Users
from app.models.studentsModel import Students
from app.models.coursesModel import Courses
from app.models.resultModel import Results


from app.views import __namespaces__


authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# Create an instance of Api
api = Api(title='Students Api',
        version='1.0',
        description='Students Management Api',
        contact='octavio.suarezdiaz@gmail.com',
        doc='/explorer',
        authorizations=authorizations
        )

# Adding all namespace for swagger
for namespace in __namespaces__:
    api.add_namespace(namespace)


def create_app(settings_module):

    app = Flask(__name__)
    CORS(app)
    
    flask_bcrypt  = Bcrypt(app)

    app.config.from_object(settings_module)

    # Push app context to current stack context for extensions
    app.app_context().push()

    # Initialize database
    db.init_app(app)

    # Initialize migration manager
    migrate.init_app(app, db)

    # Add routes
    for rule in view_rules:
        app.add_url_rule(
            rule.path,
            view_func=jwt_required(rule.view, rule.auth_provider),
            methods=rule.methods
        )

    for rule in view_rules_nonauth:
        app.add_url_rule(
            rule.path,
            view_func=rule.view,
            methods=rule.methods
        )

    # Initialize Flask-RESTx API
    api.init_app(app)

    # Register custom error handlers
    register_error_handlers(app)

    @app.route("/home/")
    def home():
        return render_template('landing.html')   
 

    @app.route("/ping")
    def ping():
        return "pong"

    return app


def register_error_handlers(app):

    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify('Internal server error'), 500

    @app.errorhandler(400)
    def handle_400_error(e):
        return jsonify('Bad request'), 400

    @app.errorhandler(401)
    def handle_401_error(e):
        return jsonify('Unauthorized'), 401

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify('Forbidden error'), 403

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify('Method not allowed'), 405

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify('Not Found error'), 404
    
    @app.errorhandler(ForbiddenException)
    def handle_forbiden_exception(e):
        return jsonify(str(e)), 403

    @app.errorhandler(UnauthorizedException)
    def handle_unauthorized_exception(e):
        return jsonify(str(e)), 401

    @app.errorhandler(ObjectNotFoundException)
    def handle_object_not_found_error(e):
        return jsonify(str(e)), 404

    @app.errorhandler(BadRequestException)
    def handle_bad_request_exception(e):
        return jsonify(str(e)), 400

    @app.errorhandler(InternalServerErrorException)
    def handle_internal_server_error_exception(e):
        return jsonify(str(e)), 500

