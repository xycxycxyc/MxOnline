from django.db import models

from apps.users.models import BaseModel


# 这里写城市类。主要是为了后期能够手动添加城市
class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name='城市名')
    desc = models.CharField(max_length=200, verbose_name='描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name
    # 魔法方法：重写__str__ 方法，创建实例时能显示实例创建的名称

    def __str__(self):
        # 要注意，这里return的值一定要存在，为none时，可能会引起异常
        return self.name


class CourseOrg(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所在城市')
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='描述')
    tag = models.CharField(default='全国知名', max_length=10, verbose_name='机构标签')
    category = models.CharField(default='pxjg', verbose_name='机构类别', max_length=4,
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')))
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', max_length=100)
    address = models.CharField(max_length=150, verbose_name='机构地址')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')

    is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    def get_courses(self):
        # from apps.courses.models import Course  # 在这里调用是为了避免循环引用
        # courses = Course.objects.filter(course_org=self)
        # courses = self.course_set.all()  # 使用外键反向取数据(取出课程机构org的所有课程）org是course的外键
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')

    age = models.IntegerField(default=18, verbose_name='年龄')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()