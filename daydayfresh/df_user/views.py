from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import UserInfo
from hashlib import sha1

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
        if UserInfo.objects.filter(uname = username)[0].upwd == pwd_s1:#用户名存在，密码正确
            rememberusername = request.POST.get('rememberusername','')
            red = HttpResponseRedirect('/user/user_center_info/')
            if rememberusername == 'on':
                red.set_cookie('uname',username)
                return red
            else:
                red.set_cookie('uname','',max_age = -1)
                return red
        else:#用户名存在，密码错误
            context = {'title':'登录','user_error':0,'pwd_error':1,'username':username,'password':pwd}
            return render(request,'df_user/login.html',context)


def user_center_info(request):
    context = {'title': '用户中心'}
    return render(request,'df_user/user_center_info.html',context)

def user_center_order(request):
    context = {'title': '用户中心'}
    return render(request,'df_user/user_center_order.html',context)

def user_center_site(request):
    context = {'title': '用户中心'}
    return render(request,'df_user/user_center_site.html',context)





# Create your views here.
