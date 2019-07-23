
from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path('register/', register),
    path('login/', login),
    re_path(r'^$', index),
    path('index/', index),
    path('register_store/', register_store),
    path('add_goods/', add_goods),
    path('list_goods/', list_goods),
    path('goods_des/', goods_des),
]
urlpatterns += [
    path('base/', base),

]