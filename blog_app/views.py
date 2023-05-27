from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages


# Create your views here.
# -------------------------------------------------------------------------------------------------------

def Home(req):
    context = {}
    return render(req, "index.html", context)






