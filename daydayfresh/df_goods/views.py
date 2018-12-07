from django.shortcuts import render,redirect
from .models import GoodsInfo,TypeInfo

def detail(request,pid,id):
    type = TypeInfo.objects.get(pk = pid)
    goods_new = GoodsInfo.objects.filter(gtype_id = pid).order_by('-id')[0:2]
    good = GoodsInfo.objects.get(pk = id)
    context = {'goods_new':goods_new,'type':type,'good':good}
    return render(request,'df_goods/detail.html',context)

def index(request):
    type1 = TypeInfo.objects.get(pk=1)
    goods1_new = type1.goodsinfo_set.order_by('-id')[0:4]#最新
    goods1_click = type1.goodsinfo_set.order_by('-gclick')[0:4]#最热

    type2 = TypeInfo.objects.get(pk=2)
    goods2_new = type2.goodsinfo_set.order_by('-id')[0:4]#最新
    goods2_click = type2.goodsinfo_set.order_by('-gclick')[0:4]#最热

    type3 = TypeInfo.objects.get(pk=3)
    goods3_new = type3.goodsinfo_set.order_by('-id')[0:4]#最新
    goods3_click = type3.goodsinfo_set.order_by('-gclick')[0:4]#最热

    type4 = TypeInfo.objects.get(pk=4)
    goods4_new = type4.goodsinfo_set.order_by('-id')[0:4]#最新
    goods4_click = type4.goodsinfo_set.order_by('-gclick')[0:4]#最热

    type5 = TypeInfo.objects.get(pk=5)
    goods5_new = type5.goodsinfo_set.order_by('-id')[0:4]#最新
    goods5_click = type5.goodsinfo_set.order_by('-gclick')[0:4]#最热

    type6 = TypeInfo.objects.get(pk=6)
    goods6_new = type6.goodsinfo_set.order_by('-id')[0:4]#最新
    goods6_click = type6.goodsinfo_set.order_by('-gclick')[0:4]#最热
    context = {'goods1_new':goods1_new,'goods1_click':goods1_click,'goods2_new':goods2_new,'goods2_click':goods2_click,
               'goods3_new':goods3_new,'goods3_click':goods3_click,'goods4_new':goods4_new,'goods4_click':goods4_click,
               'goods5_new':goods5_new,'goods5_click':goods5_click,'goods6_new':goods6_new,'goods6_click':goods6_click,}
    return render(request,'df_goods/index.html',context)

def list(request,id):
    type = TypeInfo.objects.get(pk = id)
    goods = GoodsInfo.objects.filter(gtype_id = id).order_by('-id')
    goods_new = goods[0:2]
    print(goods)
    context = {'goods':goods,'goods_new':goods_new,'type':type}
    return render(request,'df_goods/list.html',context)

# Create your views here.
