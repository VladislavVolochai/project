from . import views
from django.conf.urls import url


urlpatterns = [

	url(r'^get_requests/$', views.get_requests, name='get_requests'),

	url(r'^get_mock/(?P<group>\w*)$', views.get_mock, name='get_mock'),
	

]