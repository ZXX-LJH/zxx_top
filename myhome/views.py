from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from myadmin import models
from django.core.urlresolvers import reverse
from mypro.settings import BASE_DIR
from django.db.models import Q
from django.core.paginator import Paginator
import os


# 前台首页
def index(request):
    # 获取所有的以及分类
    data = models.Cates.objects.filter(pid = 0)

    # 获取当前以及分类下的所有二级分类
    for i in data:
        i.sub = models.Cates.objects.filter(pid = i.id)

    context = {'data': data}
    return render(request, 'myhome/index.html', context)
# 前台列表页
def list(request):
    cateid = request.GET.get('catetype','') # 一级分类提交的数据
    goodid = request.GET.get('goodtype', '') # 二级分类提交的数据
    sortid = request.GET.get('sorttype', '') # 搜索分类提交的数据
    print(cateid)
    print(goodid)
    print(sortid)

    '''
    [
        'name':'点心/蛋糕',
            'sub':[
                'name':'点心','goodslist':[
                        goodsobject,goodsobject
                    ],
                'name':'蛋糕','goodslist':[
                        goodsobject,goodsobject
                    ]
                ],
        'name':'饼干/膨化','sub':['name':'饼干','goodslist':[goodsobject,goodsobject],'name':'膨化','goodslist':[goodsobject,goodsobject]]
    ]
    '''
    # 获取所有的商品信息
    data1 = models.Goods.objects.all()  # 所有商品
    # 获取所有的标签
    data2 = models.Cates.objects.filter(pid = 0)  #　所有一级标签
    for i in data2:
        i.sub = models.Cates.objects.filter(pid = i.id) # 一级标签下嵌套所有二级标签

    data3 = "" # 某一级标签下的所有子类标签
    listvar1 =[]
    if cateid == '0':  # 全部
        pass
    elif cateid:  # 如果点击了一级标签
        # 获取请求 cateid 的所有子标签
        data3 = models.Cates.objects.filter(pid = cateid)  # 传递给二级标签的数据
        for i in data3:
            for j in models.Goods.objects.filter(Q(cateid = i.id)):
                listvar1.append(j)
            # for i in len(listvar2):
            #     listvar1.append(i)
            # data1 = models.Goods.objects.filter(Q(cateid = i.id))
        data1 = listvar1  # 指定一级标签下的指定二级标签
        # print(listvar1)

    if goodid:  # 如果点击了二级标签
        data1 = models.Goods.objects.filter(cateid = goodid)  # 指定二级下的所有商品

    # ======================  搜索  ====================
    if sortid == 'index':
        pass
    elif sortid == 'new':
        data1 = models.Goods.objects.filter(status = 0)
    elif sortid == 'remai':
        data1 = models.Goods.objects.filter(status = 1)
    elif sortid == 'price':
        data1 = models.Goods.objects.filter(price__gt = 0).order_by('price')
        print('data1', data1)
        if cateid:
            for i in data3:
                print('data2', data1)
        if goodid:
            data1 = data1.filter(cateid = goodid)
            print('data3', data1)
    elif sortid == 'clicknum':
        data1 = models.Goods.objects.filter(clicknum__gt = 0).order_by(clicknum)
    elif sortid == 'ordernum':
        data1 = models.Goods.objects.filter(ordernum__gt = 0).order_by(ordernum)

    # ======================  分页  ====================
    paginator = Paginator(data1, 12)
    p = request.GET.get('p', 1)
    data1 = paginator.page(p)

    context = {'goodslist':data1,'cateslist_one':data2, 'cateslist_two':data3, 'cateid':cateid,"goodid":goodid, 'sortid':sortid}
    return render(request, 'myhome/list.html', context)

# 登录页
def login(request):

    if request.method == 'GET':
        return render(request, 'myhome/login.html')
    elif request.method == 'POST':
        # print(request.POST['verifycode'])
        # print(request.session['verifycode'])
        if request.POST['verifycode'] == request.session['verifycode']:
            phone = request.POST['phone']
            user = models.Users.objects.get(phone = phone)
            mark = check_password(request.POST['password'],user.password)
            if mark:
                # 用户和密码都输入正确
                # 在session 中存入登录凭证
                request.session['VipUser'] = {'username':user.username, 'phone':user.phone, 'uid':user.id,'pic_url': user.pic_url}
                # print(request.session['VipUser'])
                # print(request.session['VipUser']['pic_url'])
                return HttpResponse('<script>alert("登录成功");location.href="' + reverse('myhome_index') + '"</script>')
            else:
                return HttpResponse('<script>alert("密码不正确，请重新登录");location.href="' + reverse('myhome_login') + '"</script>')
        else:
            return HttpResponse('<script>alert("验证码错误");location.href="' + reverse('myhome_login') + '"</script>')
    # return HttpResponse('login')
# 退出
def logout(request):
    if request.session['VipUser']:
        request.session['VipUser'] = ''
        print("退出成功")
        return HttpResponse('<script>alert("退出登录");location.href="' + reverse('myhome_index') + '"</script>')
    else:
        return HttpResponse('<script>alert("早已退出登录");location.href="' + reverse('myhome_index') + '"</script>')
def cart(request):
    return render(request, 'myhome/cart.html')

def meilanx(request):
    id = request.GET.get('id')
    # print('id = ', id , type(id))
    info = models.Goods.objects.filter(id = int(id))
    # print(info, type(info))
    context = {'goods': info,"id":id }
    return render(request, 'myhome/meilanx.html', context)

def cartadd(request):
    # 商品id  商品数量 用户id
    gid = request.GET.get('gid')
    num = int(request.GET.get('num'))
    uid = request.session['VipUser']['uid']

    goods = models.Goods.objects.get(id = gid)
    user = models.Users.objects.get(id = uid )

    # 检查当前的商品是否已经存在购物车
    res = models.Cart.objects.filter(uid = user).filter(goodsid = goods)
    if res.count():
        for i in res:  # 查询集  ==============  *** 有坑 *** =  =============
            i.num += num
            i.save()
        print(gid, '****************************')
    else:
        cart = models.Cart(goodsid = goods, uid = user, num = num)
        cart.save()
        print(num, '****************************')

    return JsonResponse({'error':0,'msg':'加入购物成功'})

def order(request):
    # 是否登录
    if request.session['VipUser']:
        pass
    else:
        return HttpResponse('<script>alert("请先登录");location.href="' + reverse('myhome_login') + '"</script>')

    # 接收 cartids
    cartids = eval(request.GET.get('cartids'))  # 获得商品的编号  ['10', '8', '2', '3']
    nums = eval(request.GET.get('nums'))  # 商品的购买数量
    totalPrice = request.GET.get('totalPrice')

    # 将cartids 中字符串转成 整形
    for i in range(0, len(cartids)):
        cartids[i] = int(cartids[i])

    # 获取对应的购物车数据
    for i in cartids:
        good = models.Goods.objects.get(id = i) # 通过 商品编号获得 货物对象
        # 通过货物对象 修改 购物车中的数量
        cart = models.Cart.objects.get(goodsid = good)
        cart.num = int(nums[cartids.index(i)])
        cart.save()

    # 获得商品标号对应的对象
    data = models.Goods.objects.filter(id__in = cartids)
    # print(models.Address.objects.filter(isChecked = True))  # <QuerySet []>
    if models.Address.objects.filter(isChecked = True):
        address = models.Address.objects.filter(isChecked = True)
    else:
        # 如果没有默认地址，则选择第一条数据
        address = models.Address.objects.all()[0:1]
    # 分配数据
    print(address)
    context = {'data':data, 'cartids':cartids, 'nums':nums, 'totalPrice':totalPrice, 'address':address}
    return render(request,'myhome/order.html',context)

def address(request):
    # username = request.session['VipUser']['username']  # 获得用户明
    # print(username)
    print('地址首页')
    # 获取所有的地址信息
    addinfo = models.Address.objects.all()
    context = {'addinfo':addinfo}
    return render(request, 'myhome/address.html', context)
# 修改默认地址
def set_def_address(request):
    id = int(request.GET.get('id'))
    print('id = ', id)

    # 修改之前的默认地址
    address = models.Address.objects.get(isChecked = True)
    print(address.isChecked, '*******')
    address.isChecked = False
    print(address.isChecked, '*******')
    address.save()

    # 将提交的ｉｄ作为默认
    address = models.Address.objects.get(id = id)
    address.isChecked = True
    address.save()

    return JsonResponse({'data':id})

def add_address(request):
    if request.method == 'GET':
        return render(request, 'myhome/addaddress.html')
    elif request.method == 'POST':
        print('添加地址')
        data = request.POST.dict()

        username = request.session['VipUser']['username']
        # print(username)
        user = models.Users.objects.get(username = username)  # 获得用户

        # 实例化地址对象
        address = models.Address()
        address.uid = user
        address.shr = data['shr']
        address.shdh = data['shdh']
        address.sheng = data['sheng']
        address.shi = data['shi']
        address.xian = data['xian']
        address.info = data['info']
        address.idChecked = True
        address.save()
        return HttpResponse('<script>alert("添加地址成功");location.href="' + reverse('myhome_address') + '"</script>')

def address_delete(request):
    id = request.GET.get('id','0')  # 获取地址的id
    print('删除地址')
    address = models.Address.objects.filter(id = int(id))
    address.delete()

    # addinfo = models.Address.objects.all()
    # context = {'addinfo':addinfo}
    # return render(request, 'myhome/address.html', context)
    return HttpResponse('<script>alert("删除成功");location.href="' + reverse('myhome_address') + '"</script>')

def getcitys(request):
    # 获取请求的id参数
    upid = request.GET.get('id')
    print(upid)
    # values()：一个对象构成一个字典，然后构成一个列表返回
    data = models.Citys.objects.filter(upid=upid).values()

    # [object,object,object]

    # [{},{},{}]
    return JsonResponse(list(data),safe=False)

def myorder(request):
    # 如果用户登录了
    if request.session['VipUser']:
        # request.session['VipUser'] = {'username':user.username, 'phone':user.phone, 'uid':user.id,'pic_url': user.pic_url}
        # 通过用户手机号获得用户
        user = models.Users.objects.filter(phone = request.session['VipUser']['phone'])
        # print('user = ', user)
        # 通过用户获得购物车中的数据
        cart = models.Cart.objects.filter(uid = user)  # 外键  需要一个用户对象

        # 加载魔板
        context = {'cart': cart}
        # 返回数据
        return render(request, 'myhome/myorder.html', context)
    else:
        return HttpResponse('<script>alert("请先登录");location.href="' + reverse('myhome_login') + '"</script>')
# 计算购物的价格
def countprice(request):
    id = request.GET.get('id') # 商品号
    num = request.GET.get('num')  # 商品数量
    good = models.Goods.objects.get(id = int(id))

    # 修改购物车中的数量
    cart = models.Cart.objects.get(goodsid = good)
    cart.num = int(num)
    cart.save()

    price = good.price
    res = price * int(num)
    return JsonResponse({'countprice':res})
# 注册用户
def register(request):
    if request.method == 'GET':
        return render(request, 'myhome/register.html')
    elif request.method == 'POST':
        # 判断手机号是否已存在
        try:
            # 冒错则说明不存在指定用户
            if models.Users.objects.get(phone = request.POST['phone']):
                return HttpResponse('<script>alert("手机号码已存在，请重新注册");location.href="' + reverse('myhome_register') + '"</script>')
        except:
        # 判断验证码是否正确
            if request.POST.get('verifycode') == request.session['verifycode']:
                # 获取表单提交的数据
                data = request.POST.dict()
                print(data)
                # 实例化会员类
                user = models.Users()
                user.username = 'user_' + data['phone']
                user.password = make_password(data['password'], None, 'pbkdf2_sha256')
                user.phone = data['phone']
                # 写进数据库
                user.save()
                # 清楚session
                request.session['verifycode'] = ""
                return HttpResponse('<script>alert("注册成功");location.href="' + reverse('myhome_login') + '"</script>')
            else:
                return HttpResponse('<script>alert("验证码输入错误");location.href="' + reverse('myhome_register') + '"</script>')
# 检查手机是否存在
def phone_check(request):
        phone = request.GET.get('phone')
        num = models.Users.objects.get(phone = phone)
        # print(num.phone)
        # num = 1
        if num:
            return JsonResponse({'error':1,'msg':'手机号码已被注册'})
        else:
            return JsonResponse({'error':0,'msg':'手机号码未被注册'})
    # return HttpResponse('phone_check')

def member(request):
    return render(request, 'myhome/member.html')
# 订单首页
def dingdan(request):
    # 是否登录
    if request.session['VipUser']:
        pass
    else:
        return HttpResponse('<script>alert("请先登录");location.href="' + reverse('myhome_login') + '"</script>')

    # print(request.path)
    # if request.path == '/myhome/dingdan/':
    #     # username = request.session['VipUser']['username']
    #     # user = models.Users.objects.get(username = username)
    #     # dingdan = models.Order.models.filter(uid = user)
    #     # context = {'dingdan': dingdan}
    #     # return render(request, 'myhome/member.html', context)
    #     return HttpResponse('换个方式访问')


    # 存在重复提交的情况
    cartids = request.GET.get('cartids', '0')  # 获得订单中货物的id
    # 通过 提交的 cartids 去查看购物车虫检测是否还存在数据 (取一个id 就行了)
    print(cartids, len(cartids))  # 1,4,7 5
    username = request.session['VipUser']['username']  # 获得用户名
    user = models.Users.objects.get(username = username)  # 用户

    # try: # 购物车中不存在某商品 则说明重复提交
    #     check = models.Cart.objects.get(id = int(cartids[0]))
    # except:
    #     # 获取订单
    #     order = models.Order.objects.filter(uid = user)  # 多条数据
    #     # 获取订单详情
    #     orderinfo = models.OrderInfo.objects.filter(orderid__in = order)
    #     # print(orderinfo, len(orderinfo))
    #     context = {'dingdan': order, "dingdaninfo":orderinfo}
    #     return render(request, 'myhome/dingdan.html', context)

    # dingdan
    totalprice = request.GET.get('totalPrice')  # 获得总价格
    shr = request.GET.get('shr')  #
    shdh = request.GET.get('shdh')
    sheng = request.GET.get('sheng')
    shi = request.GET.get('shi')
    xian = request.GET.get('xian')

    # 实例化订单模型
    dingdan = models.Order()
    dingdan.uid = user
    dingdan.shr = shr
    dingdan.shdh = shdh
    dingdan.shdz = sheng + ' >> ' + shi + ' >> ' + xian
    dingdan.totalprice = totalprice
    dingdan.save()

    order = models.Order.objects.last()
    # print(cartids, len(cartidss))  # 1,4,7 5

    for id in cartids.split(','):  # 注意是字符串
        # 实例化订单详情
        dingdaninfo = models.OrderInfo()
        # 获得购物车数据
        good = models.Goods.objects.get(id = int(id))
        cart = models.Cart.objects.get(goodsid = good)
        # 通过 id 获得商品
        print(id, type(id), type(int(id)))
        good = models.Goods.objects.filter(id = int(id))  # 查询集
        for j in good:
            price = j.price  # 获得商品价格
            pic_url = j.pic_url  # 获得商品图片
            print(price)

        # 通过商品获得购物车
        cart = models.Cart.objects.filter(goodsid = good)
        for j in cart:
            # 获取购物车数据中的数量
            num = j.num
            print(num)
            # 修改购物车中的数据 ( 数量 )
            print(j.num, '******************')
            j.num -= num
            # 如果购物车中的数量小于等于0 则删除购物车中的数据
            if j.num <= 0:
                j.delete()

        dingdaninfo.orderid = order
        dingdaninfo.goodsid = id
        dingdaninfo.price = price
        dingdaninfo.num = num
        dingdaninfo.pic_url = pic_url

        # 循环保存
        dingdaninfo.save()
        return HttpResponse('<script>location.href="' + reverse('myhome_dingdaninfo') + '"</script>')

def dingdaninfo(request):
    username = request.session['VipUser']['username']  # 获得用户名
    user = models.Users.objects.get(username = username)  # 用户
    # 为什么不用 all 这里是获得当前用户的数据  而不是所有用户的数据  前台列表
    # 获取订单
    order = models.Order.objects.filter(uid = user)  # 多条数据
    # 获取订单详情
    orderinfo = models.OrderInfo.objects.filter(orderid__in = order)
    # print(orderinfo, len(orderinfo))
    context = {'dingdan': order, "dingdaninfo":orderinfo}
    return render(request, 'myhome/dingdan.html', context)

def dingdan_delete(request):
    id = request.GET.get('id')
    print(id, type(id))
    dingdan = models.OrderInfo.objects.get(id = int(id))
    dingdan.delete()
    return HttpResponse('<script>alert("订单删除成功");location.href="' + reverse('myhome_dingdaninfo') + '"</script>')

def userinfo(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)

        username = request.session['VipUser']['username']
        user = models.Users.objects.get(username = username)

        user.username = data['username']
        user.phone = data['phone']
        user.sex = data['sex']
        user.age = data['age']
        user.email = data['email']
        user.save()
        return HttpResponse('<script>alert("修改个人信息成功");location.href="' + reverse('myhome_userinfo') + '"</script>')


    # 是否登录
    if request.session['VipUser']:
        pass
    else:
        return HttpResponse('<script>alert("请先登录");location.href="' + reverse('myhome_login') + '"</script>')

    # 活儿用户名
    username = request.session['VipUser']['username']
    user = models.Users.objects.filter(username = username)
    context = {'user':user}
    return render(request, 'myhome/userinfo.html', context)
