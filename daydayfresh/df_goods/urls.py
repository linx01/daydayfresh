from django.urls import re_path,include
from df_goods import views

urlpatterns = [
    re_path(r'^detail/(\d+)/(\d+)/$',views.detail),
    re_path(r'^index/$',views.index),
    re_path(r'^list/(\d+)/$',views.list),

]