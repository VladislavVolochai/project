from django.apps import AppConfig
from django.conf import settings


class MockServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mock_service'
