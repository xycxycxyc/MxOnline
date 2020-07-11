from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.users.forms import LoginForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            # user_name = request.POST.get('username', '')
            # password = request.POST.get('password', '')
            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 用于通过用户和密码查询用户是否存在,成功的话就会返回一个我们定义的user对象，返回为None时表示
            user = authenticate(username=user_name, password=password)
            from apps.users.models import UserProfile
            # 1. 通过用户名查询到用户
            # 2. 需要先对明文密码加密在通过加密之后的密码在数据库中查询
            # 3. 这种方式虽然可以完成用户名和密码的校验，但是对代码的后期维护不友好
            # user = UserProfile.objects.get(username=user_name, password=password)
            if user is not None:
                # 查询到用户,下面是登录逻辑
                login(request, user)
                # 登陆成功之后应该怎么返回页面
                # return render(request, 'index.html')  # 跳转后url地址不发生变化，所以这里使用重定向的类
                return HttpResponseRedirect(reverse('index'))
            else:
                # 未查询到用户
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})

# Create your views here.
