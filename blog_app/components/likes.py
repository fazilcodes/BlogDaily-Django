from django_unicorn.components import UnicornView
from blog_app.models import BlogPostDB
from django.contrib.auth.models import User

class LikesView(UnicornView):
    post: BlogPostDB = None
    liked_by: User = None
    no_of_likes = 0
    liked = False

    def mount(self):
        self.post = BlogPostDB.objects.get(id=self.blogid)
        if self.request.user.is_authenticated:
            self.liked_by = User.objects.get(username=self.request.user)
        else:
            self.liked_by = None
        self.no_of_likes = self.post.likes.count()
        return super().mount()
    
    def like_post(self):
        if self.liked_by in self.post.likes.all():
            self.post.likes.remove(self.liked_by)
            self.liked = False
        else:
            self.post.likes.add(self.liked_by)
            self.post.save()
            self.liked = True
        
        self.no_of_likes = self.post.likes.count()
