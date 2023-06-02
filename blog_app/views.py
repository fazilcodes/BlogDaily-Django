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


def SignUp(req):
    context = {}
    if req.method == 'POST':
        name = req.POST.get("name")
        email = req.POST.get("email")
        password = req.POST.get("password")
        confirm_password = req.POST.get("confirm_password")

        if password == confirm_password:
           if User.objects.filter(username=name).exists() :
               messages.info(req, "Username Already Taken")
               return redirect('SignUp')
           elif User.objects.filter(email=email).exists():
                messages.info(req, "An Account Already Exist in this Email")
                return redirect("Signin")
           else:
               user = User.objects.create_user(username=name, email=email, password=password)
               user.save()

               user_login = auth.authenticate(username=name, password=password)
               auth.login(req, user_login)

            #Creating a Profile for the New User


    return render(req, "LoginRegister.html", context)


def Profile(req):
    context = {}
    return render(req, "profile.html", context)


def Post(req):
    context = {}
    return render(req, "post.html", context)


def Addblog(req):
    context = {}
    return render(req, 'blog.html', context)
    







