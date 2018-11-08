from django.conf.urls import url
from . import views

urlpatterns = [
    #首页
    url(r'^index/$', views.index,name='myhome_index'),
    # 列表
    url(r'^list/$', views.list,name='myhome_list'),
    url(r'^login/$', views.login,name='myhome_login'),
    url(r'^logout/$', views.logout,name='myhome_logout'),
    url(r'^cart/$', views.cart,name='myhome_cart'),
    url(r'^meilanx/$', views.meilanx,name='myhome_meilanx'),
    url(r'^cartadd/$', views.cartadd,name='myhome_cartadd'),

    url(r'^order/$', views.order,name='myhome_order'),
    url(r'^address/$', views.address,name='myhome_address'),
    url(r'^set_def_address/$', views.set_def_address,name='myhome_set_def_address'),
    url(r'^address_delete/$', views.address_delete,name='myhome_address_delete'),
    url(r'^getcitys/$', views.getcitys,name='myhome_getcitys'),


    url(r'^add_address/$', views.add_address,name='myhome_add_address'),
    url(r'^myorder/$', views.myorder,name='myhome_myorder'),
    url(r'^countprice/$', views.countprice,name='myhome_countprice'),

    url(r'^register/$', views.register,name='myhome_register'),
    url(r'^phonecheck/$', views.phone_check,name='myhome_phone_check'),
    url(r'^memeber/$', views.member,name='myhome_member'),

    url(r'^dingdan/$', views.dingdan, name = 'myhome_dingdan'),
    url(r'^dingdaninfo/$', views.dingdaninfo, name = 'myhome_dingdaninfo'),
    url(r'^dingdan_delete/$', views.dingdan_delete, name = 'myhome_dingdan_delete'),




    url(r'^userinfo/$', views.userinfo, name = 'myhome_userinfo'),





]
