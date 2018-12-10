from django.shortcuts import render
from .models import OrderInfo

def order(request):
    return render(request,'df_order/place_order.html')

def address(request):
    name = request.POST['name']
    print('hello')
    address = request.POST['address']
    mailcode = request.POST['mailcode']
    cellphone = request.POST['cellphone']
    context = {'name':name,'address':address,'mailcode':mailcode,'cellphone':cellphone}
    return render(request,'df_order/place_order.html',context)

# Create your views here.
