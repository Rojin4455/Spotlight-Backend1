from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import JSONField

User = get_user_model()


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    total_likes = models.IntegerField(null=True, blank=True, default=0)
    total_dislikes = models.IntegerField(null=True, blank=True, default=0)
    total_comments = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.title
    
class BlogContent(models.Model):
    CONTENT_TYPES = [
        ('heading', 'Heading'),
        ('text', 'Paragraph'),
        ('code', "Code Block"),
        ('image','Image')
    ]

    blog = models.ForeignKey(Blog, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20,choices=CONTENT_TYPES)
    order = models.IntegerField()
    content_data = JSONField()
    image_url = models.URLField(max_length=500, null=True, blank=True)
    


    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.blog.title} - {self.content_type}"
    

# class BlogLike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     blog = models.ForeignKey(Blog, related_name='likes', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'blog']

#     def save(self, *args, **kwargs):
        
#         if not self.pk:
#             self.blog.total_likes = (self.blog.total_likes or 0) + 1
#             self.blog.save()
#         super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         self.blog.total_likes = (self.blog.total_likes or 1) - 1
#         self.blog.save()
#         super().delete(*args, **kwargs)        
#     def __str__(self):
#         return f"{self.user.username} likes {self.blog.title[:10] if len(self.blog.title) > 10 else self.blog.title}..."

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        
        if not self.pk:
            print("total comment vedsdede: current ", self.blog.total_comments)
            self.blog.total_comments = (self.blog.total_comments or 0) + 1
            self.blog.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.blog.total_comments = (self.blog.total_comments or 1) - 1
        self.blog.save()
        super().delete(*args, **kwargs)    

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title[:10] if len(self.blog.title) > 10 else self.blog.title}..."
    


class BlogReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_reactions')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')

    def save(self, *args, **kwargs):
        
        existing_reaction = None
        if self.pk:
           try:
                existing_reaction = BlogReaction.objects.get(pk=self.pk)
           except BlogReaction.DoesNotExist:
                existing_reaction = None
        if existing_reaction:
            if existing_reaction.reaction == 'like':
                self.blog.total_likes = (self.blog.total_likes or 1) - 1
            elif existing_reaction.reaction == 'dislike':
                self.blog.total_dislikes = (self.blog.total_dislikes or 1) - 1

        if self.reaction == 'like':
            self.blog.total_likes = (self.blog.total_likes or 0) + 1
        elif self.reaction == 'dislike':
            self.blog.total_dislikes = (self.blog.total_dislikes or 0) + 1

        self.blog.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.reaction == 'like':
            self.blog.total_likes = (self.blog.total_likes or 1) - 1
        elif self.reaction == 'dislike':
            self.blog.total_dislikes = (self.blog.total_dislikes or 1) - 1

        self.blog.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} reacted {self.blog.title[:10] if len(self.blog.title) > 10 else self.blog.title}..."

    



