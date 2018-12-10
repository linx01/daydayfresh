from django.contrib import admin
from .models import CartInfo
class CartInfoAdmin(admin.ModelAdmin):
	list_display = ['id','user','good','count']
admin.site.register(CartInfo,CartInfoAdmin)
# Register your models here.
