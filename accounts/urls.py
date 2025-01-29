from django.urls import path
from .views import *

urlpatterns = [
    path('user/signup/', RegistrationView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('admin/login/', AdminLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('get-users/', UsersView.as_view()),
    path('toggle-user-status/<int:id>/',UserStatusView.as_view()),
]