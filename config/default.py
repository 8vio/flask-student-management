import os

SECRET_KEY = os.environ.get('SECRET_KEY')
TOKEN_EXPIRES = os.environ.get('TOKEN_EXPIRES')

PROPAGATE_EXCEPTIONS = True

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS',
    False
)
SHOW_SQLALCHEMY_LOG_MESSAGES = os.environ.get(
    'SHOW_SQLALCHEMY_LOG_MESSAGES',
    False
)

ERROR_404_HELP = False
