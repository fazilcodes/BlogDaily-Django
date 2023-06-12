from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfileDB, BlogPostDB

import random




# Create your views here.
# -------------------------------------------------------------------------------------------------------

def Home(req):

    profile = None
    blogs = list(BlogPostDB.objects.all())
    random.shuffle(blogs)

    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user)
        profile = UserProfileDB.objects.get(user=logged_in_user)
        

    context = {'profile': profile, 'blogs': blogs}
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


def  Signin(req):
    if req.method == 'POST':
        username = req.POST.get('signin_username')
        password = req.POST.get('signin_password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(req, user)
            return redirect('home')
        else:
            messages.info(req, "Invalid Credentials")
            return redirect("signin")
    
    return render(req, "LoginRegister.html")


def Logout(req):
    auth.logout(req)
    return redirect('signin')


def Profile(req, pk):

    user_object = User.objects.get(username=pk)
    profile = UserProfileDB.objects.get(user=user_object)

    blogs = BlogPostDB.objects.filter(author=req.user).order_by('-id')[:4]

    context = {'profile': profile, 'blogs': blogs}
    return render(req, "profile.html", context)


def Post(req, id):

    profile = None
    blog = BlogPostDB.objects.get(id=id)

    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user.username)
        profile = UserProfileDB.objects.get(user=logged_in_user)


    context = { 'blog': blog, 'profile':profile }
    return render(req, "post.html", context)


@login_required(login_url="signup")
def Addblog(req):

    user_object = User.objects.get(username=req.user.username)
    profile = UserProfileDB.objects.get(user=user_object)
    blogs = BlogPostDB.objects.filter(author=req.user).order_by('-blog_date')

    context = {'profile': profile, 'blogs': blogs}

    return render(req, 'blog.html', context)


def AddBlog_Ajax(req):

    author_profile = UserProfileDB.objects.get(user=req.user )

    if req.method == 'POST':
        author = req.user
        author_profile = author_profile
        title = req.POST.get("title")
        caption = req.POST.get("caption")
        image = req.FILES.get("image")
        category = req.POST.get("category")

        if not title or not caption or not category or not image:
            return JsonResponse({'success': False, 'errors': 'Incomplete form data'})

        else:
            addblog = BlogPostDB.objects.create(author=author, author_profile=author_profile, title=title, caption=caption, blog_image=image, category=category)
            addblog.save()

            response_data = {
                'success': True,
                'msg': 'Data Saved',
                'title': addblog.title,
                'category': addblog.category,
                'blog_image': addblog.blog_image.url,
                'id': addblog.id
            }

            return JsonResponse(response_data)
        

# --------Update Views----------------

def Updateprofile(req, id):

    profile = UserProfileDB.objects.get(id=id)

    if req.method == 'POST':
        if req.FILES.get('update_image') is None:
            image = profile.profile_image
        else:
            image = req.FILES.get('update_image')
        
        name = req.POST.get('update_name')
        bio = req.POST.get('update_bio')
        profession = req.POST.get('update_profession')

        profile.profil_name = name
        profile.bio = bio
        profile.profession = profession
        profile.profile_image = image
        profile.save()

        return redirect('profile', pk=profile.user)

    context = {'profile': profile}
    return render(req, 'updateprofile.html', context)


def Updateblog(req, id):

    blog = BlogPostDB.objects.get(id=id)

    if req.method == 'POST':
        if req.FILES.get('popup_image') is None:
            image = blog.blog_image
        else:
            image = req.FILES.get('popup_image')

        title = req.POST.get('popup_title')
        category = req.POST.get('popup_category')
        caption = req.POST.get('popup_caption')

        blog.title = title
        blog.caption = caption
        blog.category = category
        blog.blog_image = image
        blog.save()

        print("Form submitted")
        return redirect('addblog')

    context = {"blogid": blog}
    return render(req, 'updateblog.html', context)

           







