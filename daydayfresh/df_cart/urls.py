from django.urls import re_path,include
from df_cart import views

urlpatterns = [
    re_path(r'^$',views.cart),
    re_path(r'^(\d+)/(\d+)/$',views.add),
    re_path(r'^edit/(\d+)/(\d+)/$',views.edit),
    re_path(r'^delete/(\d+)/$',views.delete),
]