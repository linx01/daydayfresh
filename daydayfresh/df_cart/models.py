from django.db import models

class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)
    good = models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    count = models.IntegerField()
    # 默认管理器
    objects = models.Manager()
# Create your models here.
