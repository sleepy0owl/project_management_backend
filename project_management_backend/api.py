from django.urls import path
from user_management.views import test_get, create_user
urls = [
    path('test/get/', test_get),
    path('user/create/', create_user)
]