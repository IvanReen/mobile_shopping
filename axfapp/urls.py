from django.urls import path
from axfapp.views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('market/', market, name='market'),
    path('cart/', cart, name='cart'),
    path('mine/', mine, name='mine'),
]