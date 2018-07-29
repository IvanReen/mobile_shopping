from django.urls import path, re_path
from axfapp.views import *

urlpatterns = [
    path('home/', home, name='home'),
    re_path('market/(\d+)/(\d+)/(\d+)/', market, name='market'),
    path('cart/', cart, name='cart'),
    re_path('changecart/(\d+)/', changecart, name='changecart'),
    path('saveoredr/', saveoredr, name='saveoredr'),


    path('mine/', mine, name='mine'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    # 验证账号
    path('checkuserid/', checkuserid, name='checkuserid'),
    path('quit/', quit, name='quit')
]