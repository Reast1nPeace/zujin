from django.shortcuts import render,redirect,reverse,HttpResponse
from .forms import UserRegisterForm,UserLoginForm
from .models import UserProfile,UserMessage,ZuHao,ZuHaoWan,OrderInfo,DingDanInfo,ChongZhiInfo,FenLeiInfo
from .utils import recommend
from django.db.models import Q
from tools.decorators import login_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate,logout,login
from django.http import JsonResponse
from datetime import datetime
from django.views.generic import View
from django.core.mail import send_mail
# Create your views here.
from django.views.decorators.cache import cache_page
from random import randrange


# Create your views here.

#生成邀请码的函数
def get_random_code(code_length):
    code_source = '2134567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    for i in range(1000):
        code = ''
        for i in range(code_length):
            str = code_source[randrange(0,len(code_source))]
            code += str
            # code += choice(code_source)
        if len(UserProfile.objects.filter(bryqm=code)) == 0:
            return code

def user_register(request):
    # 注册
    if request.method == 'GET':
        pt_order_obj = OrderInfo.objects.all().first()
        # 这里实例化forms类，目的不是为了验证，而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'register.html', locals())
    else:
        pt_order_obj = OrderInfo.objects.all().first()
        msg = ''
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            username = user_register_form.cleaned_data['username']
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            tryqm = request.POST.get('tryqm', '')
            if tryqm != '':
                #判断该邀请码是否存在
                is_exist = UserProfile.objects.filter(bryqm=tryqm).first()
                if not is_exist:
                    username = request.POST.get('username')
                    email = request.POST.get('email')
                    password = request.POST.get('password')
                    msg = '该邀请码不存在'
                    return render(request, 'register.html', locals())
                else:
                    tr = UserProfile.objects.filter(bryqm=tryqm).first()
                    tr.money += 8
                    tr.save()
                    UserMessage.objects.create(message_user=username,message_content='您填写了账户['+ tr.username +']的邀请码，ta获得8元的返利，推荐自己的邀请码给别人注册，您也可以获得返利哟')
                    UserMessage.objects.create(message_user=tr.username,message_content='账户['+ username +']填写了您的邀请码，您获得了8元的返利')

            a = UserProfile()
            #随机生成一个6位数的邀请码
            bryqm = get_random_code(6)
            a.username = username
            a.set_password(password)
            a.email = email
            a.bryqm = bryqm
            a.tryqm = tryqm
            a.save()
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # 将登录用户赋值给 request.user
                return redirect(reverse('users:index'))
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            return render(request, 'register.html', locals())

class UserLoginView(View):
    # 登录
    def get(self, request):
        pt_order_obj = OrderInfo.objects.all().first()
        # 这里实例化forms类，目的不是为了验证，而是为了使用验证码
        user_login_form = UserLoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        ret = {'status': '', 'msg': ''}
        is_gly = request.POST.get('is_gly')
        # print(is_gly)
        # print(type(is_gly))
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if str(user.is_superuser).lower() != is_gly:
                ret['status'] = 'error'
                ret['msg'] = '账户名或者密码错误'
                return JsonResponse(ret)
            else:
                login(request, user)  # 将登录用户赋值给 request.user
                ret['status'] = 'ok'
                return JsonResponse(ret)
        else:
            ret['status'] = 'error'
            ret['msg'] = '账户名或者密码错误'
            return JsonResponse(ret)

def user_logout(request):
    # 退出登录
    logout(request)
    return redirect(reverse('users:user_login'))

def index(request):
    if request.user.username == "":
        zuhao_list = ZuHao.objects.filter(fb_status=True,yz_status=False).order_by('-add_time')[0:8]
    else:
        pass
        #zuhao_list = get_user_recommand(request.user.username)
        zuhao_list = recommend(request.user.username)
    # 首页
    a = 'index'
    pt_order_obj = OrderInfo.objects.all().first()
    zuhao_fl_list = FenLeiInfo.objects.all()
    
    zuhaowan_list = ZuHaoWan.objects.all()[0:8]
    return render(request, 'index.html', locals())

@login_decorator
def fb_list(request):
    # 已租赁列表
    a = 'fb_list'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    limit = request.GET.get('limit', '')
    if limit != '':
        br_fb_list = ZuHao.objects.filter(fb_user=request.user.username, yz_status=True).values('title', 'game_name', 'area', 'server', 'money',
                                       'zh','pwd','hours','zy_time').order_by('-add_time')
        # 分页功能
        page = request.GET.get('page', '')
        pa = Paginator(br_fb_list, limit)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        pages = list(pages)
        ret = {'data': pages, 'count': br_fb_list.count(), 'code': 0}
        return JsonResponse(ret)
    return render(request, 'fb_list.html', locals())

@login_decorator
def fb_list_wzl(request):
    # 尚未租赁列表
    a = 'fb_list'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    limit = request.GET.get('limit', '')
    if limit != '':
        br_fb_list = ZuHao.objects.filter(fb_user=request.user.username, yz_status=False).values('title', 'game_name', 'area', 'server', 'money',
                                       'fb_status','zh','pwd').order_by('-add_time')
        # 分页功能
        page = request.GET.get('page', '')
        pa = Paginator(br_fb_list, limit)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        pages = list(pages)
        ret = {'data': pages, 'count': br_fb_list.count(), 'code': 0}
        return JsonResponse(ret)
    return render(request, 'fb_list_wzl.html', locals())

@login_decorator
def fb_add(request):
    # 添加租赁
    a = 'fb_list'
    if request.method == 'GET':
        zuhao_fl_list = FenLeiInfo.objects.all()
        return render(request, 'fb_add.html', locals())
    else:
        ret = {'msg': ''}
        title = request.POST.get('title', '')
        game_name = request.POST.get('game_name', '')
        area = request.POST.get('area', '')
        server = request.POST.get('server', '')
        money = request.POST.get('money', '')
        zh = request.POST.get('zh', '')
        pwd = request.POST.get('pwd', '')
        ZuHao.objects.create(fb_user=request.user.username, title=title, game_name=game_name, area=area, server=server, money=money, zh=zh, pwd=pwd)
        ret['msg'] = 'ok'
        return JsonResponse(ret)


def bz_list(request):
    # 本站租赁列表
    a = 'bz_list'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    limit = request.GET.get('limit', '')
    keyword = request.GET.get('keyword', '')
    game_name = request.GET.get('game_name', '')
    print('keyword',keyword)
    if limit != '':
        bz_fb_list = ZuHao.objects.filter(fb_status=True,yz_status=False)
        if keyword:
            bz_fb_list = bz_fb_list.filter(title__icontains=keyword)
        if game_name:
            bz_fb_list = bz_fb_list.filter(game_name=game_name)
        bz_fb_list = bz_fb_list.values('id', 'title', 'game_name', 'area', 'server',
                                                                 'money').order_by('-add_time')
        # 分页功能
        page = request.GET.get('page', '')
        pa = Paginator(bz_fb_list, limit)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        pages = list(pages)
        ret = {'data': pages, 'count': bz_fb_list.count(), 'code': 0}
        return JsonResponse(ret)
    return render(request, 'bz_list.html', locals())

import time
@login_decorator
def bz_look(request):
    # 租赁详情页
    a = 'bz_list'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    if request.method == 'GET':
        bz_id = request.GET.get('bz_id')
        hours = request.GET.get('hours')
        bz_info = ZuHao.objects.filter(id=bz_id).first()
        sum_money = str(round(float(bz_info.money) * float(hours), 2))
        return render(request, 'bz_look.html', locals())
    else:
        ret = {'msg': '','ye': ''}
        bz_id = request.POST.get('bz_id')
        title = request.POST.get('title')
        fb_user = request.POST.get('fb_user')
        money = request.POST.get('money')
        hours = request.POST.get('hours')
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        hours = float(hours)
        money = float(money)
        user_obj = UserProfile.objects.filter(username=request.user.username).first()
        if money * hours <= float(user_obj.money):
            user_obj.money = round(user_obj.money - round(money * hours, 2),2)
            user_obj.save()
            user_obj = UserProfile.objects.filter(username=request.user.username).first()
            ret['msg'] = 'ok'
            ret['ye'] = user_obj.money
            UserMessage.objects.create(message_user=request.user.username,
                                       message_content='您租用了'+fb_user+'的[' + title + ']'+ str(hours) +'个小时，账户余额为：' + str(user_obj.money) + '元')
            user_obj1 = UserProfile.objects.filter(username=fb_user).first()
            #发邮件
            user_obj1_email = user_obj1.email
            send_mail(
                '账号租赁平台',
                '%s在%s租用了您的账号%s,共%s个小时，租赁结束请即使修改密码！' % (request.user.username,str(now_time),title,str(hours)),
                '1035743330@qq.com',
                [user_obj1_email],
                fail_silently=False,
            )

            new_money = user_obj1.money + round(money * hours, 2)
            user_obj1.money = new_money
            user_obj1.save()
            UserMessage.objects.create(message_user=fb_user,
                                       message_content=request.user.username + '租用您的[' + title + ']'+ str(hours) +'个小时，您的账户增加'+ str(round(money * hours, 2)) +'元，余额为：' + str(new_money) + '元')
            bz_info = ZuHao.objects.filter(id=bz_id).first()
            bz_info.yz_status = True
            bz_info.zy_time = now_time
            bz_info.hours = hours
            bz_info.save()
            DingDanInfo.objects.create(zyr=request.user.username,fb_user=fb_user,title=bz_info.title,
                                       game_name=bz_info.game_name,area=bz_info.area,server=bz_info.server,
                                       money=bz_info.money,zh=bz_info.zh,pwd=bz_info.pwd,hours=hours,zy_time=now_time)
            

        else:
            ret['msg'] = '付款失败，账户余额不足'
        return JsonResponse(ret)

@login_decorator
def add_hours(request):
    # 输入租赁的小时数
    if request.method == 'GET':
        bz_id = request.GET.get('bz_id')
        return render(request, 'add_hours.html', locals())
    else:
        ret = {'msg':''}
        hours = request.POST.get('hours')
        fhours = float(hours)
        if fhours <= 0:
            ret['msg'] = '租赁小时数必须大于0'
        else:
            ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def yfkdd_list(request):
    # 已付款订单
    a = 'yfkdd_list'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    limit = request.GET.get('limit', '')
    if limit != '':
        yfkdd_list = DingDanInfo.objects.filter(zyr=request.user.username)
        yfkdd_list = yfkdd_list.values('title', 'game_name', 'area', 'server',
                                        'money','zyr','fb_user','zh','pwd','hours','zy_time').order_by('-add_time')
        # 分页功能
        page = request.GET.get('page', '')
        pa = Paginator(yfkdd_list, limit)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        pages = list(pages)
        ret = {'data': pages, 'count': yfkdd_list.count(), 'code': 0}
        return JsonResponse(ret)
    return render(request, 'yfkdd_list.html', locals())

def wz_list(request):
    # 外站租赁列表
    a = 'wz_list'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    limit = request.GET.get('limit', '')
    if limit != '':
        wz_list = ZuHaoWan.objects.values('title', 'game_name', 'area', 'server',
                                                                 'money', 'url')
        # 分页功能
        page = request.GET.get('page', '')
        pa = Paginator(wz_list, limit)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        pages = list(pages)
        ret = {'data': pages, 'count': wz_list.count(), 'code': 0}
        return JsonResponse(ret)
    return render(request, 'wz_list.html', locals())

@login_decorator
def cz(request):
    # 充值
    a = 'cz'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    if request.method == 'GET':
        user_obj = UserProfile.objects.filter(username=request.user.username).first()
        return render(request, 'cz.html', locals())
    else:
        ret = {'msg': ''}
        money = request.POST.get('money')
        fmoney = float(money)
        if fmoney <= 0:
            ret['msg'] = '充值金额必须大于0'
        else:
            ChongZhiInfo.objects.create(username=request.user.username,money=money)

            ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def userinfo(request):
    # 个人信息
    a = 'userinfo'
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    if request.method == 'GET':
        user = request.user
        return render(request, 'userinfo.html', locals())
    else:
        ret = {'status': '0', 'msg': ''}
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')

        user_obj = UserProfile.objects.filter(id=request.user.id).first()
        y_username = user_obj.username  # 原来的用户名
        y_email = user_obj.email  # 原来的邮箱
        if username == '' or email == '':
            ret['status'] = 'null'
            ret['msg'] = '账户名和邮箱号不能为空'
        elif y_username != username or y_email != email:
            if y_username != username:
                username_is_exist = UserProfile.objects.filter(username=username)
                if username_is_exist:
                    ret['status'] = 'username'
                    ret['msg'] = '该用户名已经存在，请换一个\n'
            if y_email != email:
                email_is_exist = UserProfile.objects.filter(email=email)
                if email_is_exist:
                    ret['status'] = 'email'
                    ret['msg'] = '该邮箱已经被使用，请换一个'


            def ValidateEmail(email):
                from django.core.validators import validate_email
                from django.core.exceptions import ValidationError
                try:
                    validate_email(email)
                    return True
                except ValidationError:
                    return False

            if not ValidateEmail(email):
                ret['status'] = 'email'
                ret['msg'] = '邮箱格式不正确，请重新输入\n'

            # 如果验证都通过
            if ret['msg'] == '':
                usermsg_list = UserMessage.objects.filter(message_user=user_obj.username)
                for usermsg in usermsg_list:
                    usermsg.message_user = username
                    usermsg.save()
                zuhao_list = ZuHao.objects.filter(fb_user=user_obj.username)
                for zuhao in zuhao_list:
                    zuhao.fb_user = username
                    zuhao.save()
                cz_list = ChongZhiInfo.objects.filter(username=user_obj.username)
                for cz in cz_list:
                    cz.username = username
                    cz.save()
                dd_list = DingDanInfo.objects.filter(zyr=user_obj.username)
                for dd in dd_list:
                    dd.zyr = username
                    dd.save()
                user_obj.username = username
                user_obj.email = email
                user_obj.save()
                ret['status'] = 'ok'
                ret['msg'] = '修改成功'
        else:
            usermsg_list = UserMessage.objects.filter(message_user=user_obj.username)
            for usermsg in usermsg_list:
                usermsg.message_user = username
                usermsg.save()
            zuhao_list = ZuHao.objects.filter(fb_user=user_obj.username)
            for zuhao in zuhao_list:
                zuhao.fb_user = username
                zuhao.save()
            user_obj.username = username
            user_obj.email = email
            user_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '修改成功'
        return JsonResponse(ret)

from django.contrib.auth.hashers import check_password


@login_decorator
def user_password(request):
    # 修改密码
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    a = 'userinfo'
    if request.method == 'GET':
        user = request.user
        return render(request, 'userpassword.html', locals())
    else:
        ret = {'status': '0', 'msg': ''}
        old_password = request.POST.get('old_password', '')
        password = request.POST.get('password', '')

        user_obj = UserProfile.objects.filter(id=request.user.id).first()
        y_password = user_obj.password  # 原来的密码
        if check_password(old_password, y_password):  # 判断原始密码是否正确
            user_obj.set_password(password)
            user_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '修改密码成功，跳转到登录页面重新登录...'
        else:
            ret['msg'] = '当前密码不正确，请重新输入'
        return JsonResponse(ret)

@login_decorator
def user_message(request):
    # 我的消息
    zuhao_fl_list = FenLeiInfo.objects.all()
    pt_order_obj = OrderInfo.objects.all().first()
    a = 'user_message'
    if request.method == 'GET':
        user_message_list = UserMessage.objects.filter(message_user=request.user.username).order_by('-add_time')
        return render(request, 'message.html', locals())

@login_decorator
def sh(request):
    # 审核发布的租赁
    if request.method == 'GET':
        limit = request.GET.get('limit', '')
        if limit != '':
            zuhao_list = ZuHao.objects.filter(fb_status=False).values('id','fb_user','title', 'game_name', 'area', 'server',
                                              'money','zh','pwd').order_by('-add_time')
            # 分页功能
            page = request.GET.get('page', '')
            pa = Paginator(zuhao_list, limit)
            try:
                pages = pa.page(page)
            except PageNotAnInteger:
                pages = pa.page(1)
            except EmptyPage:
                pages = pa.page(pa.num_pages)
            pages = list(pages)
            ret = {'data': pages, 'count': zuhao_list.count(), 'code': 0}
            return JsonResponse(ret)
        return render(request, 'sh.html', locals())
    else:
        ret = {'msg': ''}
        zuhao_id = request.POST.get('zuhao_id')
        zuhao_obj = ZuHao.objects.filter(id=zuhao_id).first()
        zuhao_obj.fb_status = True
        zuhao_obj.save()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def gl_user(request):
    # 管理用户
    if request.method == 'GET':
        limit = request.GET.get('limit', '')
        if limit != '':
            user_list = UserProfile.objects.filter(is_superuser=False).values('username', 'password', 'email', 'bryqm',
                                              'money')
            # 分页功能
            page = request.GET.get('page', '')
            pa = Paginator(user_list, limit)
            try:
                pages = pa.page(page)
            except PageNotAnInteger:
                pages = pa.page(1)
            except EmptyPage:
                pages = pa.page(pa.num_pages)
            pages = list(pages)
            ret = {'data': pages, 'count': user_list.count(), 'code': 0}
            return JsonResponse(ret)
        return render(request, 'gl_user.html', locals())
    else:
        ret = {'msg': ''}
        username = request.POST.get('username')
        UserProfile.objects.filter(username=username).delete()
        UserMessage.objects.filter(message_user=username).delete()
        ZuHao.objects.filter(fb_user=username).delete()
        ChongZhiInfo.objects.filter(username=username).delete()
        DingDanInfo.objects.filter(zyr=username).delete()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_index(request):
    pt_order_obj = OrderInfo.objects.all().first()
    return render(request, 'back_index.html',locals())

@login_decorator
def back_home(request):
    # 后台管理主页
    pt_order_obj = OrderInfo.objects.all().first()
    bz_wfb_count = ZuHao.objects.filter(fb_status=False).count()
    bz_yfb_count = ZuHao.objects.filter(fb_status=True).count()
    wz_count = ZuHaoWan.objects.all().count()
    user_count = UserProfile.objects.filter(is_superuser=False).count()  #普通用户数目

    return render(request, 'back_home.html', locals())

@login_decorator
def back_bz_yfb(request):
    # 本站已发布租赁列表
    if request.method == 'GET':
        limit = request.GET.get('limit', '')
        if limit != '':
            zuhao_list = ZuHao.objects.filter(fb_status=True).values('id','fb_user','title', 'game_name', 'area', 'server',
                                              'money','zh','pwd','yz_status').order_by('-add_time')
            # 分页功能
            page = request.GET.get('page', '')
            pa = Paginator(zuhao_list, limit)
            try:
                pages = pa.page(page)
            except PageNotAnInteger:
                pages = pa.page(1)
            except EmptyPage:
                pages = pa.page(pa.num_pages)
            pages = list(pages)
            ret = {'data': pages, 'count': zuhao_list.count(), 'code': 0}
            return JsonResponse(ret)
        return render(request, 'back_bz_yfb.html', locals())

@login_decorator
def back_bz_yfb_edit(request):
    # 本站已发布租赁编辑
    if request.method == 'GET':
        zulin_id = request.GET.get('zulin_id')
        zulin_obj = ZuHao.objects.filter(id=zulin_id).first()
        zuhao_fl_list = FenLeiInfo.objects.all()
        return render(request, 'back_bz_yfb_edit.html' ,locals())
    elif request.method == 'POST':
        ret = {'msg': ''}
        zulin_id = request.POST.get('zulin_id')
        title = request.POST.get('title')
        game_name = request.POST.get('game_name')
        area = request.POST.get('area')
        money = request.POST.get('money')
        server = request.POST.get('server')
        zh = request.POST.get('zh')
        pwd = request.POST.get('pwd')
        zulin_obj = ZuHao.objects.filter(id=zulin_id).first()
        zulin_obj.title = title
        zulin_obj.game_name = game_name
        zulin_obj.area = area
        zulin_obj.money = money
        zulin_obj.server = server
        zulin_obj.zh = zh
        zulin_obj.pwd = pwd
        zulin_obj.save()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_bz_yfb_del(request):
    # 本站已发布租赁删除
    if request.method == 'POST':
        ret = {'msg': ''}
        zuhao_id = request.POST.get('zuhao_id')
        ZuHao.objects.filter(id=zuhao_id).delete()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_fl(request):
    # 租赁分类列表
    if request.method == 'GET':
        limit = request.GET.get('limit', '')
        if limit != '':
            fl_list = FenLeiInfo.objects.values('id','name')
            # 分页功能
            page = request.GET.get('page', '')
            pa = Paginator(fl_list, limit)
            try:
                pages = pa.page(page)
            except PageNotAnInteger:
                pages = pa.page(1)
            except EmptyPage:
                pages = pa.page(pa.num_pages)
            pages = list(pages)
            ret = {'data': pages, 'count': fl_list.count(), 'code': 0}
            return JsonResponse(ret)
        return render(request, 'back_fl.html', locals())

@login_decorator
def back_fl_add(request):
    # 添加分类
    if request.method == 'GET':
        return render(request, 'back_fl_add.html' ,locals())
    elif request.method == 'POST':
        ret = {'msg': ''}
        name = request.POST.get('name', '')
        if name == '':
            ret['msg'] = '分类名称不能为空'
            return JsonResponse(ret)
        name_is_exist = FenLeiInfo.objects.filter(name=name)
        if name_is_exist:
            ret['msg'] = '该分类名称已存在，请重新输入'
        else:
            FenLeiInfo.objects.create(name=name)

            ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_fl_edit(request):
    if request.method == 'GET':
        fl_id = request.GET.get('fl_id')
        fl_obj = FenLeiInfo.objects.filter(id=fl_id).first()
        return render(request, 'back_fl_edit.html' ,locals())
    elif request.method == 'POST':
        ret = {'msg': ''}
        fl_id = request.POST.get('fl_id')
        name = request.POST.get('name', '')
        fl_obj = FenLeiInfo.objects.filter(id=fl_id).first()
        y_fl_name = fl_obj.name
        if name == '':
            ret['msg'] = '分类名称不能为空'
            return JsonResponse(ret)
        if y_fl_name != name:
            name_is_exist = FenLeiInfo.objects.filter(name=name)
            if name_is_exist:
                ret['msg'] = '该分类名称已存在，请重新输入'
                return JsonResponse(ret)
        fl_obj.name = name
        fl_obj.save()
        zuhao_list = ZuHao.objects.filter(game_name=y_fl_name)
        for zuhao in zuhao_list:
            zuhao.game_name = name
            zuhao.save()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_fl_del(request):
    # 删除分类
    if request.method == 'POST':
        ret = {'msg': ''}
        name = request.POST.get('name')
        FenLeiInfo.objects.filter(name=name).delete()
        zuhao_list = ZuHao.objects.filter(game_name=name)
        for zuhao in zuhao_list:
            zuhao.game_name = ''
            zuhao.save()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_wz_edit(request):
    # 编辑外站租赁
    if request.method == 'GET':
        zulin_id = request.GET.get('zulin_id')
        zulin_obj = ZuHaoWan.objects.filter(id=zulin_id).first()
        return render(request, 'back_wz_edit.html' ,locals())
    elif request.method == 'POST':
        ret = {'msg': ''}
        zulin_id = request.POST.get('zulin_id')
        title = request.POST.get('title')
        game_name = request.POST.get('game_name')
        area = request.POST.get('area')
        money = request.POST.get('money')
        server = request.POST.get('server')
        url = request.POST.get('url')
        zulin_obj = ZuHaoWan.objects.filter(id=zulin_id).first()
        zulin_obj.title = title
        zulin_obj.game_name = game_name
        zulin_obj.area = area
        zulin_obj.money = money
        zulin_obj.server = server
        zulin_obj.url = url
        zulin_obj.save()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_wz_del(request):
    # 删除外站租赁
    if request.method == 'POST':
        ret = {'msg': ''}
        zuhao_id = request.POST.get('zuhao_id')
        ZuHaoWan.objects.filter(id=zuhao_id).delete()
        ret['msg'] = 'ok'
        return JsonResponse(ret)

@login_decorator
def back_wz(request):
    # 外站租赁列表
    if request.method == 'GET':
        limit = request.GET.get('limit', '')
        if limit != '':
            zuhao_list = ZuHaoWan.objects.values('id','title', 'game_name', 'area', 'server',
                                              'money','url')
            # 分页功能
            page = request.GET.get('page', '')
            pa = Paginator(zuhao_list, limit)
            try:
                pages = pa.page(page)
            except PageNotAnInteger:
                pages = pa.page(1)
            except EmptyPage:
                pages = pa.page(pa.num_pages)
            pages = list(pages)
            ret = {'data': pages, 'count': zuhao_list.count(), 'code': 0}
            return JsonResponse(ret)
        return render(request, 'back_wz.html', locals())

@login_decorator
def back_user_info(request):
    # 个人信息
    if request.method == 'GET':
        user = request.user
        return render(request, 'back_usreinfo.html', locals())
    else:
        ret = {'status': '0', 'msg': ''}
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')

        user_obj = UserProfile.objects.filter(id=request.user.id).first()
        y_username = user_obj.username  # 原来的用户名
        y_email = user_obj.email  # 原来的邮箱
        if username == '' or email == '':
            ret['status'] = 'null'
            ret['msg'] = '账户名和邮箱不能为空'
        elif y_username != username or y_email != email:
            if y_username != username:
                username_is_exist = UserProfile.objects.filter(username=username)
                if username_is_exist:
                    ret['status'] = 'username'
                    ret['msg'] = '该账户名已经存在，请换一个\n'
            if y_email != email:
                email_is_exist = UserProfile.objects.filter(email=email)
                if email_is_exist:
                    ret['status'] = 'email'
                    ret['msg'] = '该邮箱已经被使用，请换一个\n'

            def ValidateEmail(email):
                from django.core.validators import validate_email
                from django.core.exceptions import ValidationError
                try:
                    validate_email(email)
                    return True
                except ValidationError:
                    return False

            if not ValidateEmail(email):
                ret['status'] = 'email'
                ret['msg'] = '邮箱格式不正确，请重新输入\n'


            # 如果验证都通过
            if ret['msg'] == '':
                user_obj.username = username
                user_obj.email = email
                user_obj.save()
                ret['status'] = 'ok'
                ret['msg'] = '修改成功'
        else:
            user_obj.username = username
            user_obj.email = email
            user_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '修改成功'
        return JsonResponse(ret)

@login_decorator
def back_user_password(request):
    # 修改密码
    if request.method == 'GET':
        user = request.user
        return render(request, 'back_userpassword.html', locals())
    else:
        ret = {'status': '0', 'msg': ''}
        old_password = request.POST.get('old_password', '')
        password = request.POST.get('password', '')

        user_obj = UserProfile.objects.filter(id=request.user.id).first()
        y_password = user_obj.password  # 原来的密码
        if check_password(old_password, y_password):  # 判断原始密码是否正确
            user_obj.set_password(password)
            user_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '修改密码成功，跳转到登录页面重新登录...'
        else:
            ret['msg'] = '当前密码不正确，请重新输入'
        return JsonResponse(ret)

@login_decorator
def back_order(request):
    # 管理平台其它信息
    if request.method == 'GET':
        pt_obj = OrderInfo.objects.all().first()
        return render(request, 'back_order.html', locals())
    else:
        ret = {'status': '0', 'msg': ''}
        pt_name = request.POST.get('pt_name', '')
        phone = request.POST.get('phone', '')
        gg = request.POST.get('gg', '')

        OrderInfo.objects.all().delete()
        OrderInfo.objects.create(pt_name=pt_name, phone=phone, gg=gg)

        ret['status'] = 'ok'
        ret['msg'] = '修改成功'
        return JsonResponse(ret)

@login_decorator
def back_cz(request):
    # 审核充值
    if request.method == 'GET':
        limit = request.GET.get('limit', '')
        if limit != '':
            cz_list = ChongZhiInfo.objects.filter(cz_status=False).values('id', 'username', 'money').order_by('-add_time')
            # 分页功能
            page = request.GET.get('page', '')
            pa = Paginator(cz_list, limit)
            try:
                pages = pa.page(page)
            except PageNotAnInteger:
                pages = pa.page(1)
            except EmptyPage:
                pages = pa.page(pa.num_pages)
            pages = list(pages)
            ret = {'data': pages, 'count': cz_list.count(), 'code': 0}
            return JsonResponse(ret)
        return render(request, 'back_cz.html', locals())
    else:
        ret = {'msg': ''}
        cz_id = request.POST.get('cz_id')
        cz_obj = ChongZhiInfo.objects.filter(id=cz_id).first()
        cz_obj.cz_status = True
        cz_obj.save()
        user_obj = UserProfile.objects.filter(username=cz_obj.username).first()
        user_obj.money += float(cz_obj.money)
        user_obj.save()
        user_obj = UserProfile.objects.filter(username=cz_obj.username).first()
        UserMessage.objects.create(message_user=cz_obj.username,
                                   message_content='您的账户充值了'+ cz_obj.money +'元，账户余额为：'+ str(user_obj.money) +'元')
        ret['msg'] = 'ok'
        return JsonResponse(ret)