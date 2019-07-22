from django.contrib import admin
from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path('register/', register),
    path('login/', login),
    re_path(r'^$', index),
]
