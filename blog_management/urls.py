from django.urls import path
from .views import *

urlpatterns = [
    path('create-blog/',BlogView.as_view()),
    path('get-blogs/', BlogView.as_view()),
    path('get-user-blogs/', UserBlogView.as_view()),
    path('admin/get-user-blogs/<int:userId>',AdminUserDetails.as_view()),
    path('add-user-reaction/<str:userReaction>/<int:blogId>/',HandleReactioView.as_view()),
    path('get-comments/<int:blogId>/', CommentView.as_view()),
    path('add-comment/<int:blogId>/', CommentView.as_view()),
    
    
]