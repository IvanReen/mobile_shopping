import os
import random
import time

from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from axf import settings
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

def changecart(request, flag):
    # 用户是否登录
    token = request.session.get('token')
    if token == None:
        # 没登陆
        return JsonResponse({'data':-1, 'status':'error'})


def mine(request):
    username = request.session.get('username', '未登录')



    return render(request, 'axf/mine.html', {'title':'我的', 'username':username})

from .forms.login import LoginForm
def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            # 验证密码
            nameid = f.cleaned_data['username']
            pswd = f.cleaned_data['passwd']
            try:
                user = User.objects.get(userAccount=nameid)
                if user.userPasswd != pswd:
                    return HttpResponseRedirect('/login/')
            except User.DoesNotExist as e:
                return HttpResponseRedirect('/login/')
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session['username'] = user.userName
            request.session['token'] = user.userToken
            return HttpResponseRedirect('/mine/')
        else:
            return render(request, 'axf/login.html', {'title': '登录', 'form':f, 'error':f.errors})
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {'title':'登录', 'form':f})

def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get('userAccount')
        userPasswd = request.POST.get('userPasswd')
        userName = request.POST.get('userName')
        userPhone = request.POST.get('userPhone')
        userAdderss = request.POST.get('userAdderss')
        userRank = 0
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f = request.FILES['userImg']
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + '.png')
        with open(userImg, 'wb') as fp:
            for data in f.chunks():
                fp.write(data)
        user = User.createuser(userAccount, userPasswd, userName, userPhone, userAdderss, userImg, userRank, userToken)
        user.save()
        request.session['username'] = userName
        request.session['token'] = userToken
        return HttpResponseRedirect('/mine/')
    else:
        return render(request, 'axf/register.html', {'title':'注册'})

def quit(request):
    logout(request)
    return HttpResponseRedirect('/mine/')

def checkuserid(request):
    userid = request.POST.get('userid')
    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({'data':'该用户已被注册', 'status':'error'})
    except User.DoesNotExist as e:
        return JsonResponse({'data':'可以注册', 'status':'success'})