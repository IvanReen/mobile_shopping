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

    cartlist = []
    if token := request.session.get('token'):
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)
    for p in productList:
        for c in cartlist:
            if c.productid == p.productid:
                p.num = c.productnum
                continue

    return render(request, 'axf/market.html', {'title':'闪送超市', 'leftSlider':leftSlider, 'productList':productList, 'childList':childList, 'categoryid':categoryid, 'cid':cid})

def cart(request):
    cartslist = []
    token = request.session.get('token')
    if token != None:
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount=user.userAccount)


    return render(request, 'axf/cart.html', {'title':'购物车', 'cartslist':cartslist})

def changecart(request, flag):
    # 用户是否登录
    token = request.session.get('token')
    if token is None:
        # 没登陆
        return JsonResponse({'data':-1, 'status':'error'})
    productid = request.POST.get('productid')
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken=token)
    c = None
    if flag == '0':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if carts.count() == 0:
            # 直接增加一条订单
            if product.storenums == 0:
                return JsonResponse({'data': -2, 'status': 'error'})
            c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg, product.productlongname, False)
            c.save()
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = '%.2f' % float(product.price * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, False)
                c.save()
        # 库存
        product.storenums += 1
        product.save()
        return JsonResponse({'data': c.productnum, 'price':c.productprice, 'status':'success'})


    elif flag == '1':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if carts.count() == 0:
            return JsonResponse({'data': -2, 'status':'error'})
        try:
            c = carts.get(productid=productid)
            # 修改数量和价格
            c.productnum -= 1
            c.productprice = '%.2f' % float(product.price * c.productnum)
            if c.productnum == 0:
                c.delete()
            else:
                c.save()
        except Cart.DoesNotExist as e:
            return JsonResponse({'data': -2, 'status': 'error'})
        # 库存
        product.storenums += 1
        product.save()
        return JsonResponse({'data': c.productnum, 'price':c.productprice, 'status': 'success'})

    elif flag == '2':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = '√' if c.isChose else ''
        return JsonResponse({'data': str, 'status': 'success'})
    # elif flag == '3':
    #     pass


def saveoredr(request):
    token = request.session.get('token')
    if token is None:
        # 没登陆
        return JsonResponse({'data': -1, 'status': 'error'})
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose=True)
    if carts.count() == 0:
        return JsonResponse({'data': -1, 'status': 'error'})

    oid = time.time() + random.randrange(1, 100000)
    oid = '%d' % oid
    o = Order.createorder(oid, user.userAccount,0)
    o.save()
    for item in carts:
        item.isDelete = True
        item.orderid = oid
        item.save()
    return JsonResponse({'status': 'success'})

def mine(request):
    username = request.session.get('username', '未登录')



    return render(request, 'axf/mine.html', {'title':'我的', 'username':username})

from .forms.login import LoginForm
def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if not f.is_valid():
            return render(request, 'axf/login.html', {'title': '登录', 'form':f, 'error':f.errors})
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
        f = LoginForm()
        return render(request, 'axf/login.html', {'title':'登录', 'form':f})

def register(request):
    if request.method != 'POST':
        return render(request, 'axf/register.html', {'title':'注册'})
    userAccount = request.POST.get('userAccount')
    userPasswd = request.POST.get('userPasswd')
    userName = request.POST.get('userName')
    userPhone = request.POST.get('userPhone')
    userAdderss = request.POST.get('userAdderss')
    userRank = 0
    token = time.time() + random.randrange(1, 100000)
    userToken = str(token)
    f = request.FILES['userImg']
    userImg = os.path.join(settings.MDEIA_ROOT, f'{userAccount}.png')
    with open(userImg, 'wb') as fp:
        for data in f.chunks():
            fp.write(data)
    user = User.createuser(userAccount, userPasswd, userName, userPhone, userAdderss, userImg, userRank, userToken)
    user.save()
    request.session['username'] = userName
    request.session['token'] = userToken
    return HttpResponseRedirect('/mine/')

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