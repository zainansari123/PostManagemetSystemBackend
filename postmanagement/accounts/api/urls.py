from django.urls import path
from .views import *

app_name = 'accounts_api'

urlpatterns = [
    path('login', UserLoginApiView.as_view(), name="login"),
    path('create_user', UserApiView.as_view(), name="create_user"),
    path('edit_user/<int:pk>', UserApiView.as_view(), name="edit_user"),
    path('user_list', UserApiView.as_view(), name="user_list"),
]
