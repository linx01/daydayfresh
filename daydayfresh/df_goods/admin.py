from django.contrib import admin
from .models import TypeInfo,GoodsInfo



class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gpic','gprice','gunit','gclick','gkucun','gtype','isDelete','gjianjie','gcontent']
    fields = ['gtitle','gpic','gprice','gunit','gclick','gkucun','gtype','isDelete','gjianjie','gcontent']
    list_filter = ['gtype']

class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle','isDelete']


admin.site.register(GoodsInfo,GoodsInfoAdmin)
admin.site.register(TypeInfo,TypeInfoAdmin)
# Register your models here.
