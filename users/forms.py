
from django import forms
# from captcha.fields import CaptchaField
from .models import UserProfile
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=15, error_messages={
        'required': '账户名不能为空',
    })
    email = forms.EmailField(required=True, error_messages={
        'required': '邮箱不能为空'
    })
    password = forms.CharField(required=True, min_length=6, max_length=12, error_messages={
        'required': '密码不能为空',
        'min_length': '密码至少6位',
        'max_length': '密码不能超过12位'
    })
    # captcha = CaptchaField()
    # 重写username字段的局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        print(username)
        is_exist = UserProfile.objects.filter(username=username)
        if is_exist:
            # 表示用户名已注册
            self.add_error("username", ValidationError("账户名已存在"))
        else:
            return username

    # 重写email字段的局部钩子
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = UserProfile.objects.filter(email=email)
        if is_exist:
            # 表示邮箱已注册
            self.add_error("email", ValidationError("邮箱已被注册"))
        else:
            return email



class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': '租账户名必须填写',
    })
    password = forms.CharField(required=True,min_length=6,max_length=12,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位',
        'max_length':'密码不能超过12位'
    })
    # captcha = CaptchaField()

