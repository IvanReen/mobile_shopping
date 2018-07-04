from django.shortcuts import render
from axfapp.models import *

# Create your views here.
def home(request):
    wheelList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]
    mainList = MainShow.objects.all()
    return render(request, 'axf/home.html', {'title':'主页','wheelsList':wheelList, 'navList':navList, 'mustbuyList':mustbuyList, 'shop1':shop1, 'shop2':shop2, 'shop3':shop3, 'shop4':shop4, 'mainList':mainList})

def market(request, categoryid, cid, sortid):
    leftSlider = FoodTypes.objects.all()

    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid, childcid=cid)
    # 排序
    if sortid == '1':
        productList = productList.order_by('productnum')
    elif sortid == '2':
        productList = productList.order_by('price')
    elif sortid == '3':
        productList = productList.order_by('-price')

    group = leftSlider.get(typeid=categoryid)
    childList = []
    childnames = group.childtypenames
    arr1 = childnames.split('#')
    for str in arr1:
        arr2 = str.split(':')
        obj = {'childName':arr2[0], 'childId': arr2[1]}
        childList.append(obj)
    return render(request, 'axf/market.html', {'title':'闪送超市', 'leftSlider':leftSlider, 'productList':productList, 'childList':childList, 'categoryid':categoryid, 'cid':cid})

def cart(request):
    return render(request, 'axf/cart.html', {'title':'购物车'})

def mine(request):
    return render(request, 'axf/mine.html', {'title':'我的'})