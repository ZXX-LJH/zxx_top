from django.db import models
# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# Create your models here.
# 用户表
class Users(models.Model):
    # 用户名 密码  手机号 邮箱 性别 年龄 头像 注册时间  状态
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=77)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100,null=True)
    sex = models.CharField(max_length=1,choices=((1,'男'),(0,'女')),null=True)
    age = models.IntegerField(null=True)
    pic_url = models.CharField(max_length=100,null=True)
    # 0 正常  1禁用
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

# 标签表
class Cates(models.Model):
    name = models.CharField(max_length=50)
    pid = models.IntegerField()
    path = models.CharField(max_length = 20)
    isDelete = models.BooleanField(default=False)
    # id	name 	pid		path
    # 1 	服装		０		０，
    # 2 	男装		１		０，１，
    # 3		西服 	２		０，１，２，
    # 4 	女装		１		０，１，
    # 5		裙子		４		０，１，４，
    # 6		超短裙	５		０，１，４，５，



# 商品表
class Goods(models.Model):
    title = models.CharField(max_length = 255)
    cateid = models.ForeignKey(to = 'Cates')
    price = models.FloatField()
    store = models.IntegerField()
    info = models.TextField()
    pic_url = models.CharField(max_length = 100)
    # 0 : 新发布  1 ： 热卖   2 ： 下架
    status = models.IntegerField(default = 0)
    clicknum = models.IntegerField(default = 0)
    ordernum = models.IntegerField(default = 0)
    addtime = models.TimeField(auto_now_add = True)

# 购物车
class Cart(models.Model):
    # id uid goodsid num
    uid = models.ForeignKey(to="Users")
    goodsid = models.ForeignKey(to="Goods")
    num = models.IntegerField()

# 收货地址模型
class Address(models.Model):
    uid = models.ForeignKey(to="Users")
    shr = models.CharField(max_length=50)
    shdh = models.CharField(max_length=11)
    sheng = models.IntegerField()
    shi = models.IntegerField()
    xian = models.IntegerField()
    # zhen = models.IntegerField(null=True)
    info = models.CharField(max_length=100)
    isChecked = models.BooleanField(default=False)

# 城市数据模型
class Citys(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    upid = models.IntegerField()

# 订单
class Order(models.Model):
    uid = models.ForeignKey(to="Users")
    shr = models.CharField(max_length=50)
    shdh = models.CharField(max_length=11)
    shdz = models.CharField(max_length=100)
    buytype = models.CharField(max_length=10)
    wl = models.CharField(max_length=10)  # 物流
    totalprice = models.FloatField()
    addtime = models.DateTimeField(auto_now_add=True)
    buytime = models.DateTimeField(null=True)
    # 0 新订单  1 已支付  2,已发货  3,已收货
    status = models.IntegerField(default=0)
'''
   id uid   收货人  电话号  地址 totalprice  支付方式,快递,订单创建时间,订单支付时间,状态( 0 新订单  1 支付  2发货 )
    101  993  2        1000
'''

# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="Order")
    goodsid = models.IntegerField()
    title = models.CharField(max_length=255)
    price = models.FloatField()
    pic_url = models.CharField(max_length=100)
    num = models.IntegerField()

'''
    id   orderid  goodsid  num price pic_url title
        101        2       1     500
        101        3       1     500


'''
