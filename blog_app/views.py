from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(req):
    context = {}
    return HttpResponse("Hello", context)