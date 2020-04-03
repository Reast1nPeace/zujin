from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class UserProfile(AbstractUser):
    bryqm = models.CharField(max_length=100, blank=True, verbose_name='本人邀请码')
    tryqm = models.CharField(max_length=100, blank=True, verbose_name='他人邀请码')
    money = models.FloatField(default=0, verbose_name='金额')
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

class ZuHaoWan(models.Model):
    title = models.CharField(verbose_name='标题', max_length=255)
    game_name = models.CharField(verbose_name='游戏名称', max_length=255)
    area = models.CharField(verbose_name='区域', max_length=255)
    server = models.CharField(verbose_name='服务器', max_length=255)
    money = models.CharField(verbose_name='租金', max_length=255)
    url = models.CharField(verbose_name='链接', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '外站租号信息'
        verbose_name_plural = verbose_name
        db_table = 'zuhaowan'

class ZuHao(models.Model):
    fb_user = models.CharField(verbose_name='发布用户', max_length=255)
    title = models.CharField(verbose_name='标题', max_length=255, blank=True, null=True)
    game_name = models.CharField(verbose_name='游戏名称', max_length=255, blank=True, null=True)
    area = models.CharField(verbose_name='区域', max_length=255, blank=True, null=True)
    server = models.CharField(verbose_name='服务器', max_length=255, blank=True, null=True)
    money = models.CharField(verbose_name='租金', max_length=255, blank=True, null=True)
    zh = models.CharField(verbose_name='账号', max_length=255, blank=True, null=True)
    pwd = models.CharField(verbose_name='密码', max_length=255, blank=True, null=True)
    fb_status = models.BooleanField(default=False, verbose_name="发布状态")
    yz_status = models.BooleanField(default=False, verbose_name="租用状态")
    hours = models.CharField(verbose_name='租用小时数', max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    zy_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="租赁时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '本站租号信息'
        verbose_name_plural = verbose_name

class UserMessage(models.Model):
    message_user = models.CharField(max_length=255,verbose_name="消息用户")
    message_content = models.CharField(max_length=1000,verbose_name="消息内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.message_content

    class Meta:
        verbose_name = '用户消息信息'
        verbose_name_plural = verbose_name

class OrderInfo(models.Model):
    pt_name = models.CharField(max_length=255,verbose_name="平台名称")
    phone = models.CharField(max_length=255,verbose_name="服务电话")
    gg = models.CharField(max_length=255,verbose_name="后台公告")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.pt_name

    class Meta:
        verbose_name = '平台的其它信息'
        verbose_name_plural = verbose_name

class DingDanInfo(models.Model):
    zyr = models.CharField(max_length=255,verbose_name="租用人")
    fb_user = models.CharField(verbose_name='发布用户', max_length=255)
    title = models.CharField(verbose_name='标题', max_length=255, blank=True, null=True)
    game_name = models.CharField(verbose_name='游戏名称', max_length=255, blank=True, null=True)
    area = models.CharField(verbose_name='区域', max_length=255, blank=True, null=True)
    server = models.CharField(verbose_name='服务器', max_length=255, blank=True, null=True)
    money = models.CharField(verbose_name='租金', max_length=255, blank=True, null=True)
    zh = models.CharField(verbose_name='账号', max_length=255, blank=True, null=True)
    pwd = models.CharField(verbose_name='密码', max_length=255, blank=True, null=True)
    hours = models.CharField(verbose_name='小时', max_length=255, blank=True, null=True)
    zy_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="租赁开始时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.zyr

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

class ChongZhiInfo(models.Model):
    username = models.CharField(max_length=255,verbose_name="充值账户")
    money = models.CharField(max_length=255, verbose_name='金额')
    cz_status = models.BooleanField(default=False, verbose_name="充值状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '充值信息'
        verbose_name_plural = verbose_name

class FenLeiInfo(models.Model):
    name = models.CharField(max_length=255,verbose_name="分类名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类信息'
        verbose_name_plural = verbose_name