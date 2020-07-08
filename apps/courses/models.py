from datetime import datetime  # 自带包的位置

from django.db import models  # 第三方包的位置

from apps.users.models import BaseModel    # 自己的包的位置
from apps.organizations.models import Teacher  # 引入teacher作为course的外键
# 1.设计表结构有几个重要的的点：
'''
实体1《关系》实体2
课程  章节  视频  课程资源
'''
# 2.实体的具体字段

# 3.每个字段的类型，是否必填


# 第一个实体：课程
class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师')
    name = models.CharField(verbose_name='课程名', max_length=50)
    desc = models.CharField(verbose_name='课程描述', max_length=300)
    learn_times = models.IntegerField(verbose_name='学习时长（分钟数)', default=0)
    degree = models.CharField(verbose_name='难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=5)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    category = models.CharField(verbose_name='课程类别', max_length=20, default=u"后端开发")
    tag = models.CharField(verbose_name='课程标签', max_length=10, default='')
    youneed_know = models.CharField(verbose_name='课程须知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name='老师告诉你', max_length=300, default='')

    detail = models.TextField(verbose_name='课程详情')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图', max_length=100)

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


# 第二个实体：章节
# 课程（course）与章节（Lesson）是一对多的关系，因此要在Lesson里面设置一个外键course
class Lesson(BaseModel):
    # on_delete必填字段，表示外键对用的数据被删除后，外键这一列该怎么处理，
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 级联删除
    # course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)  # 置为null
    name = models.CharField(max_length=100, verbose_name='章节名')
    learn_times = models.IntegerField(verbose_name='学习时长（分钟数)', default=0)

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name


# 第三个实体：视频（video）
class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # 级联删除
    name = models.CharField(max_length=100, verbose_name='视频名')
    learn_times = models.IntegerField(verbose_name='学习时长（分钟数)', default=0)
    url = models.CharField(max_length=200, verbose_name=u'访问地址')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


# 第四个实体：课程资源（courseresource）
class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 级联删除
    name = models.CharField(max_length=100, verbose_name='名称')
    file = models.FileField(upload_to="course/resource/%Y%m", verbose_name='下载地址', max_length=200)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
