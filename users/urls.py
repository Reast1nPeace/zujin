"""GuLiEdu URL Configuration

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
from users import views
app_name = 'users'
urlpatterns = [
    #前台
    #首页
    url(r'^index/$',views.index,name='index'),
    #注册
    url(r'^user_register/$',views.user_register,name='user_register'),
    #登录
    url(r'^user_login/$', views.UserLoginView.as_view(), name='user_login'),
    #退出登录
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    #已租赁列表
    url(r'^fb_list/$', views.fb_list, name='fb_list'),
    #尚未租赁列表
    url(r'^fb_list_wzl/$', views.fb_list_wzl, name='fb_list_wzl'),
    #添加租赁
    url(r'^fb_add/$', views.fb_add, name='fb_add'),
    #本站租赁列表
    url(r'^bz_list/$', views.bz_list, name='bz_list'),
    #租赁详情页
    url(r'^bz_look/$', views.bz_look, name='bz_look'),
    #输入租赁的小时数
    url(r'^add_hours/$', views.add_hours, name='add_hours'),
    #外站租赁列表
    url(r'^wz_list/$', views.wz_list, name='wz_list'),
    #充值
    url(r'^cz/$', views.cz, name='cz'),
    #个人信息
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    #修改密码
    url(r'^user_password/$', views.user_password, name='user_password'),
    #我的消息
    url(r'^user_message/$', views.user_message, name='user_message'),
    #已付款订单
    url(r'^yfkdd_list/$', views.yfkdd_list, name='yfkdd_list'),


    #管理员后台管理
    #审核发布的租赁
    url(r'^sh/$', views.sh, name='sh'),
    #管理用户
    url(r'^gl_user/$', views.gl_user, name='gl_user'),
    #后台管理主页
    url(r'^back_index/$', views.back_index, name='back_index'),
    url(r'^back_home/$', views.back_home, name='back_home'),
    #本站已发布租赁列表
    url(r'^back_bz_yfb/$', views.back_bz_yfb, name='back_bz_yfb'),
    #本站已发布租赁编辑
    url(r'^back_bz_yfb_edit/$', views.back_bz_yfb_edit, name='back_bz_yfb_edit'),
    #本站已发布租赁删除
    url(r'^back_bz_yfb_del/$', views.back_bz_yfb_del, name='back_bz_yfb_del'),
    #租赁分类列表
    url(r'^back_fl/$', views.back_fl, name='back_fl'),
    #添加分类
    url(r'^back_fl_add/$', views.back_fl_add, name='back_fl_add'),
    #编辑分类
    url(r'^back_fl_edit/$', views.back_fl_edit, name='back_fl_edit'),
    #删除分类
    url(r'^back_fl_del/$', views.back_fl_del, name='back_fl_del'),
    #外站租赁列表
    url(r'^back_wz/$', views.back_wz, name='back_wz'),
    #编辑外站租赁
    url(r'^back_wz_edit/$', views.back_wz_edit, name='back_wz_edit'),
    #删除外站租赁
    url(r'^back_wz_del/$', views.back_wz_del, name='back_wz_del'),
    #个人信息
    url(r'^back_user_info/$', views.back_user_info, name='back_user_info'),
    #修改密码
    url(r'^back_user_password/$', views.back_user_password, name='back_user_password'),
    #管理平台其它信息
    url(r'^back_order/$', views.back_order, name='back_order'),
    #审核充值
    url(r'^back_cz/$', views.back_cz, name='back_cz'),

]
