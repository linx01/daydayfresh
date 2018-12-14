from django.shortcuts import render,redirect
from .models import OrderInfo,OrderDetailInfo
from df_goods.models import GoodsInfo
from df_cart.models import CartInfo
from df_user.models import UserInfo
from django.db import transaction
from datetime import datetime




def order(request):
    uid = request.session['uid']
    #取得购物车列表中该用户的数据并展示
    carts = CartInfo.objects.filter(user_id = uid)
    if len(carts) == 0:
        return redirect('/')
    num = 1
    for cart in carts:
        cart.num = num
        num += 1
    user = UserInfo.objects.get(pk = uid)
    uaddress = user.uaddress
    umailcode = user.umailcode
    ureceive = user.ureceive
    umobile = user.umobile
    address = umailcode + ' ' + uaddress + ' ' + ureceive + ' ' + umobile
    context = {'request':request,'carts':carts,'address':address}
    return render(request,'df_order/place_order.html',context)

#1.从数据库拿取订单中的数据
#2.创建订单对象
#3.创建详细订单对象
#4.修改库存
#5.将数据库中保存购物车的数据删除


@transaction.atomic()
def handle_order(request):

    #创建事务的回溯点
    tran_id = transaction.savepoint()

    try:

        #得到用户资料
        user = UserInfo.objects.get(pk = request.session['uid'])
        ureceive = user.ureceive
        umailcode = user.umailcode
        uaddress = user.uaddress
        umobile = user.umobile

        #得到确认提交订单页面购物车信息
        carts = CartInfo.objects.filter(user_id = request.session['uid'])
        cart_ids = []
        total = 0

        #创建并保存订单
        order = OrderInfo()
        print(order.oid)
        order.user = user
        order.oid = datetime.now().strftime('%Y%m%d%H%M%S') + order.user.uname
        order.odate = datetime.now()
        order.oaddress = umailcode + ' ' + uaddress + ' ' + ureceive + ' ' + umobile
        order.ototal = total
        order.save()

        for cart in carts:
            # 创建详细订单
            orderdetail = OrderDetailInfo()
            #保存cart ids
            cart_ids.append(cart.id)
            #取出每一行购物车的商品，并将它与每一行详细订单的货物id挂钩
            good = GoodsInfo.objects.get(id = cart.good_id)
            orderdetail.good_id = good.id
            #取商品数量，计算库存并保存
            good_count = cart.count
            orderdetail.count = good_count
            good.gkucun = good.gkucun - good_count
            good.save()
            #取商品价格
            good_price = good.gprice
            orderdetail.price = good_price
            #计算总价
            total += good_count * good_price
            #保存订单详细信息
            orderdetail.order_id = order.oid
            orderdetail.save()

        #计算总价，再次保存订单
        order.ototal = total + 10
        order.save()
        #删除购物车
        for id in cart_ids:
            cart = CartInfo.objects.get(pk = id)
            cart.delete()
        #提交事务
        transaction.savepoint_commit(tran_id)

    except Exception as result:
        #出现错误就回退到保存点
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/user_center_order/')











