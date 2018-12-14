from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from df_user.models import UserInfo
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo,OrderDetailInfo
from hashlib import sha1
from django.core.paginator import *

def decoration_login(func):
    def login_in(request,*args,**kwargs):
        if request.session.get('uname','') != '':
            return func(request,*args,**kwargs)
        else:
            ret = HttpResponseRedirect('/user/login/')
            ret.set_cookie('url',request.get_full_path())
            return ret
    return login_in


def register(request):
    #print('register')
    context = {'title':'注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    #接收用户输入值
    uname = request.POST.get('user_name')
    upwd = request.POST.get('pwd')
    upwd2 = request.POST.get('cpwd')
    uemail = request.POST.get('email')
    #判断两次密码是否相同
    if upwd != upwd2:
        return redirect('/user/register/')
    #加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd_s1 = s1.hexdigest()
    #创建对象(创建表格的行）
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_s1
    user.uemail = uemail
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login/')

#通过ajax在register页面判断注册账号是否存在
def register_exist(request):
    username = request.GET.get('username')
    times = UserInfo.objects.filter(uname = username).count()
    return JsonResponse({'count':times})


def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'登录','username':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    username = request.POST.get('username')
    times = UserInfo.objects.filter(uname = username).count()
    if times == 0:
        # 用户名不存在
        context = {'title': '登录', 'user_error': 1, 'pwd_error': 0,'username':username}
        return render(request, 'df_user/login.html', context)
    else:
        pwd = request.POST.get('pwd')
        s1 = sha1()
        s1.update(pwd.encode('utf-8'))
        pwd_s1 = s1.hexdigest()
        users = UserInfo.objects.filter(uname = username)
        if users[0].upwd == pwd_s1:#用户名存在，密码正确
            #登录完成后在session中保存一系列用户的信息
            request.session['uname'] = username
            request.session['uemail'] = users[0].uemail
            request.session['uid'] = users[0].id
            rememberusername = request.POST.get('rememberusername','')
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            if rememberusername == 'on':
                red.set_cookie('uname',username)
            else:
                red.set_cookie('uname','',max_age = -1)
            return red
        else:#用户名存在，密码错误
            context = {'title':'登录','user_error':0,'pwd_error':1,'username':username,'password':pwd}
            return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()

    red = HttpResponseRedirect('/')
    red.set_cookie('url','/')
    red.set_cookie('goods_id','')
    return red



@decoration_login
def user_center_info(request):
    goods_id = request.COOKIES.get('goods_id','')
    if goods_id != '':
        goods_id = goods_id.split(',')
        goods = []
        for good_id in goods_id:
            good = GoodsInfo.objects.get(pk = good_id)
            goods.append(good)
    else:
        goods = goods_id
    context = {'title': '用户中心','request':request,'goods':goods}
    return render(request, 'df_user/user_center_info.html', context)

@decoration_login
def user_center_order(request,pagenumber):
    uid = request.session['uid']
    orders = OrderInfo.objects.filter(user_id = uid).order_by('-oid')
    for order in orders:
        order.details = OrderDetailInfo.objects.filter(order_id = order.oid)
        for orderdetail in order.details:
            orderdetail.total = orderdetail.count * orderdetail.price
    paginator = Paginator(orders,2)
    if pagenumber == '':
        page = paginator.page(1)
    else:
        page = paginator.page(pagenumber)
    context = {'title': '用户中心','request':request,'page':page}
    return render(request, 'df_user/user_center_order.html', context)


@decoration_login
def user_center_site(request):
    uid = request.session['uid']
    user = UserInfo.objects.get(pk = uid)
    uaddress = user.uaddress
    umailcode = user.umailcode
    ureceive = user.ureceive
    umobile = user.umobile
    address = umailcode + ' ' + uaddress + ' ' + ureceive + ' ' + umobile
    context = {'title':'用户中心','request':request,'address':address}
    return render(request, 'df_user/user_center_site.html', context)



def editaddress(request):
    uid = request.session['uid']
    user = UserInfo.objects.get(pk = uid)
    user.uaddress = request.POST['address']
    user.umailcode = request.POST['mailcode']
    user.ureceive = request.POST['name']
    user.umobile = request.POST['cellphone']
    user.save()
    return redirect('/order/')

def pay(request,oid):
    order = OrderInfo.objects.get(pk = oid)
    order.oIsPay = True
    order.save()
    return redirect('/user/user_center_order/')

# Create your views here.
