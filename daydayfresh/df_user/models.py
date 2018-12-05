
from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length = 20)
    upwd = models.CharField(max_length = 40)
    uemail = models.CharField(max_length = 30)
    ureceive = models.CharField(max_length = 20,default='')# 设置default与blank是python层面的约束，不影响数据库，不需要重新做迁移
    uaddress = models.CharField(max_length = 100,default='')
    umailcode = models.CharField(max_length = 6,default='' )
    umobile = models.CharField(max_length = 11,default='')

# Create your models here.
