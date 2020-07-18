from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from apps.organizations.models import CourseOrg
from apps.organizations.models import City
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from apps.organizations.forms import AddAskForm


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()

        all_courses = course_org.course_set.all()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=4, request=request)
        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'all_courses': courses,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()

        all_teacher = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'home'

        course_org = CourseOrg.objects.get(id=org_id)
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[0:3]
        all_teacher = course_org.teacher_set.all()[0:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,

        })


class AddAskView(View):
    # 处理用户的咨询
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)  # 提交到数据库，commit=True表示并执行，返回一个user_ask实例
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        # 热门机构排序
        hot_orgs = all_orgs.order_by('-click_nums')[0:3]  # 这个切片表示只选择点击量前三的机构展示
        # 通过机构类别对课程机构进行筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 通过所在城市对课程机构进行筛选
        city_id = request.GET.get('city', '')
        if city_id.isdigit():
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 对机构按照学习人数进行排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')  # 前面加负号表示逆序
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 统计机构的数量
        org_nums = all_orgs.count()
        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=4, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'org_nums': org_nums,
            'all_citys': all_citys,
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'hot_orgs': hot_orgs,

        })

# Create your views here.
