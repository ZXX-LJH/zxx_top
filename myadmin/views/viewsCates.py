from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from .. import models
from django.core.urlresolvers import reverse
from mypro.settings import BASE_DIR

import os


def cate_index(request):
    from django.core.paginator import Paginator

# =======================  排序  ======================
    # data = models.Cates.objects.all()
    data = models.Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths') # 是标签有序排列
    # select *, concat(path, id) as paths from types order by paths;

# ======================  分页  ====================
    paginator = Paginator(data, 10)
    # 获取请求的页数
    p = request.GET.get('p', 1)
    # 获取请求页的数据
    data = paginator.page(p)

    context = {'cateslist':data}
    return render(request,'myadmin/cates/index.html',context)


def cate_add(request):
    # user_add 使用的是两个路由， 在这里可以用一个路由代替  表单的提交方式为 post
    if request.method == 'GET':
        # 获取所有的商品分类
        data = models.Cates.objects.extra(select={'paths': 'concat(path,id)'}).order_by('paths') # 可以封装成函数
        # 分配数据
        context = {'cateslist': data}
        # 加载模板
        return render(request, 'myadmin/cates/add.html', context)
    elif request.method == 'POST':
        try:
            # 执行添加
            ob = models.Cates()
            ob.pid = request.POST.get('pid') # 获取下拉框输入的值  1
            ob.name = request.POST.get('cate') # 获取输入框输入的值
            # print(request.POST.get('cate'))
            # print(request.POST.get('pid'))

            # cate = request.POST.dict() # 2
            # for k,v in cate.items():
            #     print(k,v)

            # 判断是否为顶级分类
            if ob.pid == '0':
                ob.path = '0,'
            else:
                # 获取当前所选的分类的path
                fob = models.Cates.objects.get(id=ob.pid)
                ob.path = fob.path + ob.pid + ','
            ob.save()

            return HttpResponse('<script>alert("添加成功");location.href="' + reverse('myadmin_cate_index') + '"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="' + reverse('myadmin_cate_add') + '"</script>')


def cate_delete(request, id):
    # 获取当前标签下所有的子集个数
    num = models.Cates.objects.filter(pid=id).count()
    if num:  # 说明过存在子集
        return JsonResponse({"error":1,"msg":"it has sons, so don't delete "})
    # 有商品添加

    data = models.Cates.objects.get(id = id)
    data.delete()

    return HttpResponse('<script>alert("删除成功");location.href="' + reverse('myadmin_cate_index') + '"</script>')
    # return HttpResponse('delete')

# 一般写法
def cate_edit(request, id):
    if request.method == 'GET':
        # 通过id 获得数据库中对应的数据
        data = models.Cates.objects.get(id = id)
        # 将数据返回给  edit.html 渲染
        return render(request, 'myadmin/cates/edit.html',{'cateinfo':data})
    elif request.method == "POST":
        try:
            data = models.Cates.objects.get(id = id)
            data.name = request.POST.get('name')
            data.save()
            return HttpResponse('<script>alert("修改成功");location.href="' + reverse('myadmin_cate_index') + '"</script>')
        except:
            return HttpResponse('<script>alert("修改失败");location.href="' + reverse('myadmin_cate_edit') + '"</script>')

# ajax
def catesedit(request):
    try:
        # 根据cid获取分类对象
        ob = models.Cates.objects.get(id=request.GET.get('cid'))
        ob.name = request.GET.get('name')
        ob.save()
        return JsonResponse({'error':0,'msg':'更新成功'})
    except:
        return JsonResponse({'error':1,'msg':'更新失败'})
