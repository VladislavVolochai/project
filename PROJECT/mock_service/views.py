from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Mock, OurRequest

from urllib.parse import unquote
from datetime import datetime, timedelta
import time
import os
import json


DELETE_REQUESTS_AFTER_MINUTES = 1


def update_requests(request): 
    OurRequest.objects.filter(
        time__lte=datetime.now()-timedelta(minutes=DELETE_REQUESTS_AFTER_MINUTES)
    ).delete() # bad idea, cron needs for it

    request_url = unquote(request.get_full_path())
    request_body = unquote(request.body)

    count = OurRequest.objects.filter(url=request_url,body=request_body).count() # bad idea, cache needs for it

    OurRequest(
        method=request.method,
        url=request_url, # decoded
        body=request_body, # decoded
        encoding=request.encoding,
        headers=request.headers.__dict__['_store'],
    ).save()

    return count, request_url, request_body


@csrf_exempt
def get_mock(request, group=''):
    # if not group: Mock.objects.all()
    mocks = None
    match = None
    count = 0 # requests dublicate. Default Mock.number
    
    #request_url = unquote(request.get_full_path())
    #request_body = unquote(request.body)

    count, request_url, request_body = update_requests(request)

    if group == 'NULL':
        mocks = Mock.objects.order_by('-number').filter(
            Q(request_method='any')|Q(request_method__icontains=request.method), 
            active=True, group__active=True, number__lte=count
        ).prefetch_related('words')
    else:
        mocks = Mock.objects.order_by('-number').filter(
            Q(request_method='any')|Q(request_method__icontains=request.method), 
            active=True, group__active=True,group__slug=group, number__lte=count
        ).prefetch_related('words')

    for mock in mocks:
        words = [i.content for i in mock.words.all()]

        if mock.all_words: # Mock.all_words => 'All'
            if all(
                [i in request_url or 
                 i in request_body or 
                 i in str(request.headers.__dict__['_store']) 
                 for i in words]
                ):
                match = mock
                break
        else: # Mock.all_words => 'Any'
            if any(
                [i in request_url or 
                 i in request_body or 
                 i in str(request.headers.__dict__['_store']) 
                 for i in words]
                ):
                match = mock
                break

    if match:
        response = HttpResponse()
        response.content = match.response_content #.encode('utf-8') 
        response.status_code = match.response_status_code
        if (rh := match.response_headers): response.headers = rh
        return response

    else: # no match
        response = HttpResponse()
        response.status_code = 344
        return response


def get_requests(request):
    update_requests(request)
    qs = OurRequest.objects.all()
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False, charset='utf-8')
