from django.shortcuts import render,redirect
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from django.http import HttpResponseRedirect,JsonResponse
from django.core.paginator import *

def decoration_login(fun):
    def login_in(request,*args,**kwargs):
        if request.session.get('uname','') != '':
            print(request.session.get('uname'))
            return fun(request,*args,**kwargs)
        else:
            ret = HttpResponseRedirect('/user/login/')
            ret.set_cookie('url',request.get_full_path())
            return ret
    return login_in


@decoration_login
def cart(request):
    uid = request.session.get('uid')
    #取得购物车列表中该用户的数据并展示
    carts = CartInfo.objects.filter(user_id = uid)
    count = len(carts)
    if request.is_ajax():
        return JsonResponse({'count':count})
    #用户购买的商品列表
    else:
        context = {'request':request,'carts':carts}
        return render(request,'df_cart/cart.html',context)
        
@decoration_login
def add(request,id,count):
    uid = request.session.get('uid')   
    carts = CartInfo.objects.filter(user_id = uid).filter(good_id = id)
    if len(carts) == 0:#如果该用户未购买此商品
    #创建购物车对象并保存至数据库中
        cart = CartInfo()
        cart.user_id = uid
        cart.good_id = id
        cart.count = count
    else:#该用户已购买
        cart = carts[0]
        cart.count += int(count)
    cart.save()
    #取得购物车列表中该用户的数据并展示
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id = uid).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

def edit(request,cid,count):
    try:
        cart = CartInfo.objects.get(pk = cid)
        cart.count = int(count)
        cart.save()
        dict = {'ok':0}
    except Exception as result:
        dict = {'ok':count}
    return JsonResponse(dict)

def delete(request,cid):
    try:
        cart = CartInfo.objects.get(pk = cid)
        cart.delete()
        dict = {'ok':0}
    except Exception as result:
        print(result)
        dict = {'ok':1}
    return JsonResponse(dict)  




# Create your views here.
