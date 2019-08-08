from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import create_bookmark, index

urlpatterns = [
    path('', login_required(index), name='index'),
    path('create', login_required(create_bookmark), name='create-bookmark'),
]
