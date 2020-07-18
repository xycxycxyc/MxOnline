"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

import xadmin
from apps.organizations.views import OrgView
from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('d_login/', DynamicLoginView.as_view(), name='d_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # url与path配置url的区别是， url支持正则表达式的写法，path不支持
    url(r'^captcha/', include('captcha.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),

    # 配置上传文件的访问路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 机构相关页面
    # url(r'^org_list/', OrgView.as_view(), name='org_list'),
    # 使用inlude的方式能使url分层（org/list）
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),

]

# 编写一个view的几个步骤：
'''
1.编写view逻辑代码
2.配置url
3.修改html页面中相关的地址，比如登录的时候，登陆表单form的action要对应相应的view
'''
