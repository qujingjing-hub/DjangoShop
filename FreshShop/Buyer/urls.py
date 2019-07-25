from django.urls import path,include
from Buyer.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('index/', index),
]
urlpatterns += [
    path("base/", base),
]