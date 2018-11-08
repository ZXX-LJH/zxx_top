from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from .. import models
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from mypro.settings import BASE_DIR

import os


def cart_index(request):
    cartslist = models.Cart.objects.all()

    # ====================  分页  ==========================

    # 实例化分页类        (需要分页的数据   , 每页显示的数据)
    paginator = Paginator(cartslist, 10)
    # 获取请求的页数
    p = request.GET.get('p', 1)
    # 获取请求页的数据
    cartslist = paginator.page(p)


    context = {'cartslist': cartslist}
    return render(request, 'myadmin/carts/index.html', context)

def dingdan_index(request):
    dingdanlist = models.Order.objects.all()

    # ====================  分页  ==========================

    # 实例化分页类        (需要分页的数据   , 每页显示的数据)
    paginator = Paginator(dingdanlist, 10)
    # 获取请求的页数
    p = request.GET.get('p', 1)
    # 获取请求页的数据
    dingdanlist = paginator.page(p)


    context = {'dingdanlist':dingdanlist}
    return render(request, 'myadmin/dingdan/index.html', context)

def dingdan_info(request):
    id = request.GET.get('id')  # 订单号
    order = models.Order.objects.get(id = int(id))
    dingdaninfo = models.OrderInfo.objects.filter(orderid = order)

    context = {'dingdaninfo': dingdaninfo}
    return render(request, 'myadmin/dingdan/info.html', context)

def dingdan_edit(request, uid):
    if request.method == 'GET':
        order = models.Order.objects.get(id = uid)
        print(order)
        context = {'order':order}
        return render(request, 'myadmin/dingdan/edit.html', context)
    elif request.method == 'POST':
        data = request.POST.dict()
        # 获得该订单
        order = models.Order.objects.get(id = uid)
        order.status = data['status']
        order.save()
        return HttpResponse('<script>alert("修改成功");location.href="' + reverse('myadmin_dingdan_index') + '"</script>')
