default_app_config = 'myapp.apps.MyAppConfig'
from .celery import app as celery_app

__all__ = ('celery_app',)