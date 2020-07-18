from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, \
    RegisterGetForm, RegisterPostForm
from apps.utils.YunPian import send_single_sms
from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {
            'register_get_form': register_get_form,
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['code']

            # 用户不存在，新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.set_password(password)  # 调用此方法，保存的是加密后的密文密码，因为数据库存的是密文
            user.mobile = mobile
            user.save()
            login(request, user)
            # 登录之后跳转到首页
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                'register_post_form': register_post_form,
            })


class DynamicLoginView(View):
    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = login_form.cleaned_data['mobile']
            code = login_form.cleaned_data['code']

            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                print(existed_users)
                user = existed_users[0]
            else:
                # 用户不存在，新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)  # 生成随机明文密码
                user.set_password(password)  # 调用此方法，保存的是加密后的密文密码，因为数据库存的是密文
                user.mobile = mobile
                user.save()
            login(request, user)
            # 登录之后跳转到首页
            return HttpResponseRedirect(reverse('index'))


        else:
            d_form = DynamicLoginForm()
            return render(request, 'login.html', {'login_form': login_form,
                                                  'd_form': d_form,
                                                  'dynamic_login': dynamic_login})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json['code'] == 0:
                re_dict['status'] = 'success'
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 300) # 设置验证码五分钟过期

            else:
                re_dict['msg'] = re_json['msg']
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form
        })

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
