from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.db.models import Count
from django.db import models

from .models import UserProfileDB, BlogPostDB, CommentsDB

import random




# Create your views here.
# -------------------------------------------------------------------------------------------------------

def Home(req):

    profile = None
    blogs = list(BlogPostDB.objects.all())
    random.shuffle(blogs)
    blogs = blogs[:12]

    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user)
        profile = UserProfileDB.objects.get(user=logged_in_user)
    
    annotated_blogs = BlogPostDB.objects.annotate(
        num_likes=Count('likes'),
        num_comments=Count('commentsdb')
    )

    # Calculate a score for each blog based on likes and comments count
    annotated_blogs = annotated_blogs.annotate(score=models.F('num_likes') + models.F('num_comments'))

    # Get the top 5 blogs with the highest score
    featured_blogs = annotated_blogs.order_by('-score')[:5]

    # Randomly select a featured blog
    featured_blog = random.choice(featured_blogs) if featured_blogs else None

    context = {'profile': profile, 'blogs': blogs, 'featured_blog': featured_blog}
    return render(req, "index.html", context)


def Category_posts(req, pk):
    profile = None
    blogs = list(BlogPostDB.objects.all())
    random.shuffle(blogs)
    category_blogs = list(BlogPostDB.objects.filter(category=pk))
    random.shuffle(blogs)
    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user)
        profile = UserProfileDB.objects.get(user=logged_in_user)
    context = {'profile': profile, 'blogs': blogs, 'category_blogs': category_blogs, 'category': pk}
    return render(req, 'category_post.html', context)


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

@never_cache
def Logout(req):
    auth.logout(req)
    return redirect('home')

def Profile(req, pk):
    try:
        user_object = User.objects.get(username=pk)
        profile = UserProfileDB.objects.get(user=user_object)
    except (User.DoesNotExist, UserProfileDB.DoesNotExist, ObjectDoesNotExist):
        pass

    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user.username)
        nav_image = UserProfileDB.objects.get(user=logged_in_user)
    else:
        nav_image = None

    blogs = BlogPostDB.objects.filter(author=user_object).order_by('-id')[:4]

    context = {'profile': profile, 'blogs': blogs, 'nav_image': nav_image}
    return render(req, "profile.html", context)


def Post(req, id):

    profile = None
    blog = BlogPostDB.objects.get(id=id)
    comments = CommentsDB.objects.filter(post=id).order_by('-id')
    no_of_comments = comments.count()

    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user.username)
        profile = UserProfileDB.objects.get(user=logged_in_user)


    context = { 'blog': blog, 'profile':profile, 'comments': comments, "no_of_comments": no_of_comments }
    return render(req, "post.html", context)


@login_required(login_url="signup")
def Addblog(req):

    user_object = User.objects.get(username=req.user.username)
    profile = UserProfileDB.objects.get(user=user_object)
    blogs = BlogPostDB.objects.filter(author=req.user).order_by('-id')

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
@never_cache
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

@never_cache
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


# ----------search view----------------------

def Search(req):

    profile = None
    blogs = list(BlogPostDB.objects.all())
    random.shuffle(blogs)
    if req.user.is_authenticated:
        logged_in_user = User.objects.get(username=req.user)
        profile = UserProfileDB.objects.get(user=logged_in_user)
    
    search = req.POST.get('search_query')
    search_blogs = []
    users = []

    if req.method == 'POST' and search:
        search_blogs = list(BlogPostDB.objects.filter(Q(title__istartswith=search)))
        random.shuffle(search_blogs)
        users = list(UserProfileDB.objects.filter(Q(profil_name__istartswith=search)))
        random.shuffle(users)


    context = {'profile': profile, 'blogs': blogs, 'search_blogs': search_blogs ,'search': search, 'users': users}
    return render(req, 'search.html', context)









