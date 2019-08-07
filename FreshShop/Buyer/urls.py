from django.urls import path,include
from Buyer.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('index/', index),
    path('goods_list/', goods_list),
    path('goods_detail/', goods_detail),
    path('pay_order/', pay_order),
    path('pay_result/', pay_result),
    path('place_order/',place_order),
    path('cart/',cart),
    path('add_cart/',add_cart),
]
urlpatterns += [
    path("base/", base),
]