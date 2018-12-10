from django.db import models

#一个用户对应多个订单，将外键设置在订单类
class OrderInfo(models.Model):
	oid = models.CharField(max_length = 20,primary_key = True)
	user = models.ForeignKey('df_user.UserInfo',on_delete = models.CASCADE)
	odate = models.DateTimeField(auto_now = True)
	oIsPay = models.BooleanField(default = False)
	ototal = models.DecimalField(max_digits = 6, decimal_places = 2)
	oaddress = models.CharField(max_length = 150)

#多个订单对应多个商品，新建立一张表格保存二者的关系
class OrderDetailInfo(models.Model):
	good = models.ForeignKey('df_goods.GoodsInfo',on_delete = models.CASCADE)
	order = models.ForeignKey('OrderInfo',on_delete = models.CASCADE)
	price = models.DecimalField(max_digits = 6, decimal_places = 2)
	count = models.IntegerField()


# Create your models here.
