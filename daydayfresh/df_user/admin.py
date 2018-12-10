from django.contrib import admin
from .models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
	list_display = ['id','uname','upwd','uemail','ureceive','uaddress','umailcode','umobile']

admin.site.register(UserInfo,UserInfoAdmin)
# Register your models here.
