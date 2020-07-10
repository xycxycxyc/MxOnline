from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICE = (
    ('male', '男'),
    ('female', '女')
)


# Create your models here.
# 把每个类都共有的属性写到一个积基类里面，使用继承的方式创建子类，就可以继承共有的属性了。
# 但是这样写还有个问题，model里面定义的类在migrate的时候是会生成表的，要防止基类生成表,定义class meta, abstract = True即可
# 并且在分层设计的时候要放在最底层，因为要被高层模型引用
class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        abstract = True


# 继承原有的auth_user类，并增加新属性
class UserProfile(AbstractUser):
    # 因为必填项如果不填的话，数据库会抛出异常，因此或者设置可为空，或者设置默认值
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', choices=GENDER_CHOICE, max_length=6)
    address = models.CharField(max_length=100, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    image = models.ImageField(upload_to='head_image/%Y/%m', default='default.jpg', verbose_name='用户头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
