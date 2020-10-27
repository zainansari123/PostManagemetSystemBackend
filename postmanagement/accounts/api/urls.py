from django.urls import path
from .views import *

app_name = 'accounts_api'

urlpatterns = [
    path('login', UserLoginApiView.as_view(), name="login"),
    path('create_user', UserApiView.as_view(), name="create_user"),
]
