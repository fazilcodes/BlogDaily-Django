from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfileDB




# Create your views here.
# -------------------------------------------------------------------------------------------------------

@login_required(login_url="signup")
def Home(req):
    logged_in_user = User.objects.get(username=req.user.username)
    profile = UserProfileDB.objects.get(user=logged_in_user)

    context = {'profile': profile}
    return render(req, "index.html", context)


def SignUp(req):
    if req.method == 'POST':
        name = req.POST.get("name")
        email = req.POST.get("email")
        password = req.POST.get("password")
        confirm_password = req.POST.get("confirm_password")

        if password == confirm_password:
           if User.objects.filter(username=name).exists() :
               messages.info(req, "Username Already Taken")
               return redirect('signup')
           elif User.objects.filter(email=email).exists():
               messages.info(req, "An Account Already Exist in this Email")
               return redirect("signup")
           else:
               user = User.objects.create_user(username=name, email=email, password=password)
               user.save()

               user_login = auth.authenticate(username=name, password=password)
               auth.login(req, user_login)

               #Creating a Profile for the New User

               user_type = User.objects.get(username=name)
               user_profile = UserProfileDB.objects.create(user=user_type)
               user_profile.save()
               return redirect("home")
        else:
            messages.info("Password Does Not Match")
            return redirect("signup")


    context = {}
    return render(req, "LoginRegister.html", context)


def Profile(req, pk):

    user_object = User.objects.get(username=pk)
    profile = UserProfileDB.objects.get(user=user_object)

    context = {'profile': profile}
    return render(req, "profile.html", context)


def Post(req):
    context = {}
    return render(req, "post.html", context)


def Addblog(req):

    user_object = User.objects.get(username=req.user.username)
    profile = UserProfileDB.objects.get(user=user_object)

    context = {'profile': profile}

    return render(req, 'blog.html', context)
    







