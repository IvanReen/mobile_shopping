from django.shortcuts import render
from axfapp.models import *

# Create your views here.
def home(request):
    wheelList = Wheel.objects.all()
    return render(request, 'axf/home.html', {'title':'主页','wheelsList':wheelList})

def market(request):
    return render(request, 'axf/market.html', {'title':'闪送超市'})

def cart(request):
    return render(request, 'axf/cart.html', {'title':'购物车'})

def mine(request):
    return render(request, 'axf/mine.html', {'title':'我的'})