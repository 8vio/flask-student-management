import os

from app import create_app


settings_module = os.environ.get('APP_SETTINGS_MODULE')
app = create_app(settings_module)
