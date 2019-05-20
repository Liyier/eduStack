from .models import Publisher, Teacher
from utils.query import get_publisher_courses, has_fav
from operation.models import UserFavorite
from course.models import Course
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


class PublishersView(View):
    def get(self, request):
        # django的queryset是懒惰生成的， 而不用担心取的太多而造成数据库压力或内存压力
        all_publishers = Publisher.objects.all()
        top_publisher = all_publishers.order_by('-click_num')[:3]
        
        category = request.GET.get("category", '')
        
        # 链式查询
        if category:
            all_publishers = all_publishers.filter(category=int(category))
        
        sort_by = request.GET.get("sort_by", '')
        if sort_by:
            if sort_by == 'fav_num':
                all_publishers.order_by('-fav_num')
            elif sort_by == "course_num":
                all_publishers.order_by("-course_num")
        count = all_publishers.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_publishers, per_page=1, request=request)
        page_publishers = p.page(page)

        return render(request, "org-list.html", {
            "publishers": page_publishers,
            "count": count,
            "category": category,
            "sort_by": sort_by,
            "top_publisher": top_publisher,
            
        })
  
    
class PublisherIndexView(View):
    def get(self, request, publisher_id):
        publisher = Publisher.objects.get(id=publisher_id)
        all_teachers = publisher.teacher_set.all()
        teachers = all_teachers[:2]
        all_teacher_ids = [teacher.id for teacher in all_teachers]
        
        courses = Course.objects.filter(teacher_id__in=all_teacher_ids)[:2]
        
        return render(request, "org-detail-homepage.html", {
            "publisher": publisher,
            "teachers": teachers,
            "courses": courses,
            "has_fav": has_fav(request.user, publisher_id, 3),
            "current_page": "home"
        })
    

class UserFavView(View):

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, data_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                # 收藏类型为课程
                course = Course.objects.get(id=int(fav_id))
                course.fav_num -= 1
                if course.fav_num < 0:
                    course.fav_num = 0
                course.save()
            elif int(fav_type) == 2:
                # 收藏类型为教师
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            elif int(fav_type) == 3:
                # 收藏类型为机构
                publisher = Publisher.objects.get(id=int(fav_id))
                publisher.fav_num -= 1
                if publisher.fav_num < 0:
                    publisher.fav_num = 0
                publisher.save()
            return HttpResponse('{"status":"successed", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.data_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_num += 1
                    course.save()
                elif int(fav_type) == 2:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save()
                elif int(fav_type) == 3:
                    publisher = Publisher.objects.get(id=int(fav_id))
                    publisher.fav_num += 1
                    publisher.save()

                return HttpResponse('{"status":"successed", "msg":"取消收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"收藏出错"}', content_type='application/json')
            

class PublisherCourseView(View):
    def get(self, request, publisher_id):
        publisher = Publisher.objects.get(id=publisher_id)
        all_courses = get_publisher_courses(publisher_id=publisher_id)
        
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=2, request=request)
        page_courses = p.page(page)
        
        return render(request, "org-detail-course.html", {
            "current_page": "course",
            "all_courses": page_courses,
            "publisher": publisher,
            "has_fav": has_fav(request.user, publisher_id, 3)
        })


class PublisherDescView(View):
    def get(self, request, publisher_id):
        
        publisher = Publisher.objects.get(id=publisher_id)
        return render(request, "org-detail-desc.html", {
            "current_page": "desc",
            "publisher": publisher,
            "has_fav":  has_fav(request.user, publisher_id, 3)
        })


class PublisherTeacherView(View):
    def get(self, request, publisher_id):
        publisher = Publisher.objects.get(id=publisher_id)
        all_teachers = publisher.teacher_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=2, request=request)
        page_teachers = p.page(page)

        return render(request, "org-detail-teachers.html", {
            "current_page": "teacher",
            "page_teachers": page_teachers,
            "publisher": publisher,
            "has_fav": has_fav(request.user, publisher_id, 3)
        })