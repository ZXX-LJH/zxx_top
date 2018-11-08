from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. import models
from . viewsIndex import uploads
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q


def good_index(request):
    from django.core.paginator import Paginator

    data = models.Goods.objects.all()
    # 过滤　逻辑删除的对象
    # data = models.Goods.objects.filter(Q(status__contains=0)|Q(status__contains=1))

# ==================  搜索  ============================
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    print(types)
    print(keywords)
    if types:
        if types == 'all':
            data = data.filter(Q(title__contains=keywords)|Q(price__contains=keywords)|Q(info__contains=keywords)|Q(store__contains=keywords)|Q(clicknum__contains=keywords)|Q(ordernum__contains=keywords))
        elif types == 'status':
            # keywords == 禁用
            arr = {'新品': 0, '热卖':1,'下架':2}
            data = data.filter(status=arr[keywords])
        elif types == 'price':
            res = keywords.split('-')
            # print(res)
            data = data.filter(price__gt = int(res[0])).filter(price__lt = int(res[1]))
        elif types == 'store':
            res = keywords.split('-')
            data = data.filter(store__gt = int(res[0])).filter(store__lt = int(res[1]))
        else:
            # data = data.filter(username__contains=keywords)
            search = {types + '__contains': keywords}
            data = data.filter(**search)

    # ======================  分页  ====================
    paginator = Paginator(data, 10)
    # 获取请求的页数
    p = request.GET.get('p', 1)
    # 获取请求页的数据
    data = paginator.page(p)

    context = {'goodslist':data}

    return render(request, "myadmin/goods/index.html",context)
    # return HttpResponse("good_index")


def good_add(request):
    if request.method == "GET":
        # data = models.Cates.objects.all()
        data = models.Cates.objects.extra(select={'paths': 'concat(path,id)'}).order_by('paths') # 可以封装成函数
        return render(request,'myadmin/goods/add.html',{'cateslist':data})

    elif request.method == "POST":
        good = models.Goods()

        good.title = request.POST.get('title')
        print(good.title)
        good.info = request.POST.get('info')
        good.cateid = models.Cates.objects.get(id = request.POST.get('cateid'))  # 外键　　《－－　　对象

        good.price = request.POST.get('price')
        good.store = request.POST.get('store')
        # good.info = request.POST.get('pic_url')
        myfile = request.FILES.get('pic_url')
        if myfile:
            good.pic_url = uploads(myfile)
        else:
            return HttpResponse('<script>alert("必须上传商品主图");history.back(-1);</script>')

        # good.status = request.POST.get('status')
        # good.clicknum = 0
        # good.ordernum = 0

        good.save()

        return HttpResponse('<script>alert("添加成功！");location.href="' + reverse('myadmin_good_index') + '"</script>')
    # return HttpResponse("good_add")


def good_edit(request, pid):
    if request.method == 'GET':
        print('ceshi')
        data1 = models.Goods.objects.get(id = pid)
        data2 = models.Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths') # 是标签有序排列

        context = {'goodlist':data1,'cateslist':data2}
        print('ceshi2')
        # return HttpResponse("good_edit")
        return render(request,'myadmin/goods/edit.html' , context)
    elif request.method =='POST':
        try:
            good = models.Goods.objects.get(id = pid)
            # goodinfo = request.POST.dict()
            # goodinfo.pop('csrfmiddlewaretoken')
            # for k, v in goodinfo.items():
            #     good.k = v

            good.title = request.POST.get('title')
            good.price = request.POST.get('price')
            good.store = request.POST.get('store')
            good.info = request.POST.get('info')
            good.status = request.POST.get('status')

            myfile = request.FILES.get('pic_url')
            if myfile:
                good.pic_url = uploads(myfile)
            good.save()
            return HttpResponse('<script>alert("修改成功！");location.href ="' + reverse('myadmin_good_index') + '"</script>')
        except:
            return HttpResponse('<script>alert("修改失败！");location.href ="' + reverse('myadmin_good_edit') + '"</script>')


    # return HttpResponse("good_edit")


def good_delete(request, pid):
    # 物理删除
    data = models.Goods.objects.get(id = pid)
    data.delete()

    #　逻辑删除
    # data = models.Goods.objects.get(id = pid)
    # data.status = 2
    # data.save()

    return HttpResponse('<script>alert("删除成功");location.href="' + reverse('myadmin_good_index') + '"</script>')
