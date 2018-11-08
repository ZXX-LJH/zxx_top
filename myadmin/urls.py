"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import viewsCates,viewsGoods,viewsIndex, viewsCarts




urlpatterns = [
    #首页
    url(r'^index$', viewsIndex.index,name='myadmin_index'),
    url(r'^login/$', viewsIndex.myadminlogin, name = 'myadmin_login'),
    url(r'^verifycode/$', viewsIndex.verifycode, name = 'myadmin_verifycode'),
    url(r'^logout/$', viewsIndex.logout, name = 'myadmin_logout'),


    # 会员添加
    url(r'^user/index/$', viewsIndex.user_index, name='myadmin_user_index'),
    url(r'^user/index_edit/([0-9]+)/$', viewsIndex.user_index_edit, name='myadmin_user_indexToedit'),
    url(r'^user/add/$', viewsIndex.user_add, name='myadmin_user_add'),
    url(r'^user/register/$', viewsIndex.user_register, name='myadmin_user_register'),
    url(r'^user/edit/(?P<uid>[0-9]+)/$', viewsIndex.user_edit, name='myadmin_user_edit'),
    url(r'^user/delete/(?P<uid>[0-9]+)/$', viewsIndex.user_delete, name='myadmin_user_delete'),

    # 标签添加
    url(r'^cate/index/$', viewsCates.cate_index, name='myadmin_cate_index'),
    url(r'^cate/add/$', viewsCates.cate_add, name='myadmin_cate_add'),
    url(r'^cate/delete/(?P<id>[0-9]+)/$', viewsCates.cate_delete, name='myadmin_cate_delete'),
    url(r'^cate/edit/(?P<id>[0-9]+)/$', viewsCates.cate_edit, name='myadmin_cate_edit'),
    url(r'^cates/edit/$', viewsCates.catesedit,name='myadmin_cates_edit'),  # 发送ajax请求去修改

    # 商品添加
    url(r'^good/index/$',viewsGoods.good_index,name = 'myadmin_good_index'),
    url(r'^good/add/$',viewsGoods.good_add, name = 'myadmin_good_add'),
    url(r'^good/edit/(?P<pid>[0-9]+)/$',viewsGoods.good_edit, name = 'myadmin_good_edit'),
    url(r'^good/delete/(?P<pid>[0-9]+)/$',viewsGoods.good_delete, name = 'myadmin_good_delete'),

    # 购物车添加
    url(r'^cart/index/$',viewsCarts.cart_index,name = 'myadmin_cart_index'),

    # 订单
    url(r'^dingdan/index/$', viewsCarts.dingdan_index, name = 'myadmin_dingdan_index'),
    url(r'^dingdan/info/$', viewsCarts.dingdan_info, name = 'myadmin_dingdan_info'),
    url(r'^dingdan/edit/(?P<uid>[0-9]+)/$', viewsCarts.dingdan_edit, name='myadmin_dingdan_edit'),





]
