from django.contrib import admin
from .models import Blog, BlogContent,  Comment

admin.site.register(Blog)
admin.site.register(BlogContent)
admin.site.register(Comment)

# Register your models here.
