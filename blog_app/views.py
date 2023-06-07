from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfileDB, BlogPostDB




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

    blogs = BlogPostDB.objects.filter(author=req.user)

    context = {'profile': profile, 'blogs': blogs}
    return render(req, "profile.html", context)


def Post(req):
    context = {}
    return render(req, "post.html", context)

@login_required(login_url="signup")
def Addblog(req):

    user_object = User.objects.get(username=req.user.username)
    profile = UserProfileDB.objects.get(user=user_object)

    # if req.method == 'POST':
    #     author = req.user
    #     title = req.POST.get("title")
    #     caption = req.POST.get("caption")
    #     image = req.FILES.get("image")
    #     category = req.POST.get("category")

    #     if not title:
    #         messages.info(req, "Forgot to add Title?")
    #     elif not image:
    #         messages.info(req, "Forgot to upload Image?")
    #     elif not caption:
    #         messages.info(req, "Forgot to add caption?")
    #     elif not category:
    #         messages.info(req, "Forgot to add category?")
    #     else:
    #         messages.info("Blog Added Successfully")
    #         addblog = BlogPostDB.objects.create(author=author, title=title, caption=caption, blog_image=image, category=category)
    #         addblog.save()
    #         return redirect("home")

    blogs = BlogPostDB.objects.filter(author=req.user)

    context = {'profile': profile, 'blogs': blogs}

    return render(req, 'blog.html', context)


def AddBlog_Ajax(req):

    if req.method == 'POST':
        author = req.user
        title = req.POST.get("title")
        caption = req.POST.get("caption")
        image = req.FILES.get("image")
        category = req.POST.get("category")

        if not title or not caption or not category or not image:
            return JsonResponse({'success': False, 'errors': 'Incomplete form data'})

        else:
            addblog = BlogPostDB.objects.create(author=author, title=title, caption=caption, blog_image=image, category=category)
            addblog.save()

            response_data = {
                'success': True,
                'msg': 'Data Saved',
                'title': addblog.title,
                'category': addblog.category,
                'blog_image': addblog.blog_image.url  # Assuming 'blog_image' is a FileField in the BlogPostDB model
            }

            return JsonResponse(response_data)
           







