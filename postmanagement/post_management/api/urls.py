from django.urls import path
from .views import *

app_name = 'task_api'

urlpatterns = [
    path('create_task', TaskApiView.as_view(), name="create_task"),
    path('entry_update/<int:pk>', TaskApiView.as_view(), name="entry_update"),
    path('user_list', TaskApiView.as_view(), name="user_list"),
]
