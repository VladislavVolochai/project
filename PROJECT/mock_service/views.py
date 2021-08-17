from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.test import override_settings

from .models import Mock, OurRequest

from urllib.parse import unquote
from datetime import datetime, timedelta
import time
import os
import json



# ############
# from django.db import connection, reset_queries
# import time
# import functools

# def query_debugger(func):
# 	@functools.wraps(func)
# 	def inner_func(*args, **kwargs):
# 		reset_queries()
# 		start_queries = len(connection.queries)
# 		start = time.perf_counter()
# 		result = func(*args, **kwargs)
# 		end = time.perf_counter()
# 		end_queries = len(connection.queries)
# 		print(f"Function : {func.__name__}")
# 		print(f"Number of Queries : {end_queries - start_queries}")
# 		print(f"Finished in : {(end - start):.2f}s")
# 		return result
# 	return inner_func
	
# @query_debugger
# def check1(): # better # prefetch_related # check with shell
# 	mocks = Mock.objects.filter(Q(request_method='any')|Q(request_method__icontains='GET') ,active=True, group__active=True).prefetch_related('words')
# 	for mock in mocks:
# 		words = [i.content for i in mock.words.all()]
	
# @query_debugger
# def check2(): # worst
# 	mocks = Mock.objects.filter(Q(request_method='any')|Q(request_method__icontains='GET') ,active=True, group__active=True)
# 	for mock in mocks:
# 		words = [i.content for i in mock.words.all()]
# ##########

def update_requests(request):
	OurRequest.objects.filter(time__lte=datetime.now()-timedelta(minutes=1)).delete() # удаляем старые

	request_url = unquote(request.get_full_path())
	request_body = unquote(request.body)

	count = OurRequest.objects.filter(url=request_url,body=request_body).count() # запрос шо щас, был ли такой недавно и скок

	OurRequest(
		#user=request.user if request.user.is_authenticated else None ,
		method=request.method,
		url=request_url, # decode
		body=request_body, # decode
		encoding=request.encoding,
		headers=request.headers.__dict__['_store'],
	).save()
	print(count) #
	return count, request_url, request_body



@csrf_exempt
def get_mock(request, group=None):
	# if not group: Mock.objects.all()
	mocks = None
	match = None

	# print(request.get_full_path())
	# mocks = Mock.objects.filter(active=True,group__active=True,group__slug=group)
	# print(request.__dict__.keys())
	# print(request.get_full_path())
	# print('scheme: ',request.scheme)
	# print('body: ',request.body)
	# print('path: ',request.path) #
	# print('path_info: ',request.path_info)
	# print('method: ',request.method)
	# print('encoding: ',request.encoding)
	# print('content_type: ',request.content_type)
	# print('content_params: ',request.content_params)
	# print('GET: ',request.GET) #
	# print('POST: ',request.POST) #
	# print('COOKIES: ',request.COOKIES)
	# print('FILES: ',request.FILES)
	# print('META: ',request.META)
	# print('headers: ',request.headers)
	# print('resolver_match: ',request.resolver_match)

	# print(request.GET.dict())
	# print(request.POST.dict())

	# print(request.headers.__dict__['_store'])
	
	count, request_url, request_body = update_requests(request)

	mocks = Mock.objects.order_by('number').filter(Q(request_method='any')|Q(request_method__icontains=request.method), active=True, group__active=True,group__slug=group, number__lte=count).prefetch_related('words') if group else Mock.objects.order_by('number').filter(Q(request_method='any')|Q(request_method__icontains=request.method) ,active=True, group__active=True, number__lte=count).prefetch_related('words')

	

	break_ = False
	for mock in mocks:
		words = [i.content for i in mock.words.all()]

		if mock.all_words:
			if all([i in request_url for i in words]) or all([i in request_body for i in words]) or all([i in str(request.headers.__dict__['_store']) for i in words]):
				match = mock
				break_ = True
		else: # неоптимально наверн
			if any([i in request_url for i in words]) or any([i in request_body for i in words]) or any([i in str(request.headers.__dict__['_store']) for i in words]):
				match = mock
				break_ = True



	if match:
		response = HttpResponse()
		response.content = match.response_content
		response.status_code = match.response_status_code
		if (rh := match.response_headers): response.headers = rh
		return response


	else: # no match
		response = HttpResponse()
		response.status_code = 344
		response.content = f'{unquote(request.get_full_path())}' ################## убрать
		return response



def get_requests(request):
	update_requests(request)

	qs = OurRequest.objects.all()
	qs_json = serializers.serialize('json', qs)
	#print(qs_json)
	return JsonResponse(qs_json, safe=False, charset='utf-8')
