from django.urls import path, re_path
from axfapp.views import *

urlpatterns = [
    path('home/', home, name='home'),
    re_path('market/(\d+)/(\d+)/(\d+)/', market, name='market'),
    path('cart/', cart, name='cart'),
    path('mine/', mine, name='mine'),
]