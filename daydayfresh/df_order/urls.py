from df_order import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^$',views.order),
    re_path(r'^handle_order/$',views.handle_order)

]