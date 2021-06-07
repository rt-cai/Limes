from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest

from limes_common.connections import ELabConnection

def index(request: WSGIRequest):
    return HttpResponse("Hello, world. You're at the core index.")

def Login(request: WSGIRequest):
    print(request.POST['username'])
    print(request.POST['password'])
    print(request.POST['id'])
    return JsonResponse({'a': 'b'})