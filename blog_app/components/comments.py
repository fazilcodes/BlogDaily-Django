from django_unicorn.components import UnicornView
from blog_app.models import BlogPostDB, UserProfileDB, CommentsDB

class CommentsView(UnicornView):
    post: BlogPostDB = None
    commented_by: UserProfileDB = None
    comments: CommentsDB = None
    comment: str = ""
    no_of_comments = 0

    def mount(self):
        self.post = BlogPostDB.objects.get(id=self.blogid)
        self.commented_by = UserProfileDB.objects.get(user=self.request.user)
        self.comments = CommentsDB.objects.filter(post=self.post.id).order_by('-id')
        self.no_of_comments = self.comments.count()
        return super().mount()
    
    def add_comment(self):
        if self.comment:
            new_comment = CommentsDB.objects.create(comment=self.comment, post=self.post, commented_by=self.commented_by)
            new_comment.save()

            self.comments = CommentsDB.objects.filter(post=self.blogid)
            self.no_of_comments = self.comments.count()
            self.comment = ""
        else:
            pass
