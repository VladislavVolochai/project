from django.apps import AppConfig
from django.conf import settings

class MockServiceConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'mock_service'

	# def ready(self):
	# 	if settings.SCHEDULER_AUTOSTART:
	# 		from .tasks import start
	# 		start()