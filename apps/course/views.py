from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from .models import Course, CourseResource, Video
from operation.models import CourseComments, UserCourse
from pure_pagination import PageNotAnInteger, Paginator
from utils.query import has_fav, get_relate_courses
from utils.auth import LoginRequiredView


class CoursesView(View):
    def get(self, request):
        courses = Course.objects.all()
        # 按照点击量排列
        top_courses = courses.order_by("-click_num")[:3]
        keyword = request.GET.get("keyword", '')
        if keyword:
            courses = courses.filter(
                Q(name__icontains=keyword) | 
                Q(teacher__name__icontains=keyword) |
                Q(teacher__publisher__name__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        sort_by = request.GET.get("sort_by", "")
        if sort_by == "":
            # 默认按照更新时间排序
            courses = courses.order_by("-update_time")
        elif sort_by == "learn_num":
            # 按照学习人数排序
            courses = courses.order_by("-learn_num")
        elif sort_by == "fav_num":
            # 按照收藏人数排序
            courses = courses.order_by("-fav_num")
        else:
            pass
            
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, per_page=6, request=request)
        page_courses = p.page(int(page))
        return render(request, "course-list.html", {
            "courses": page_courses,
            "top_courses": top_courses,
            "sort_by": sort_by,
            "keyword": keyword
        })
    
    
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_num += 1
        course.save()
        chapter_num = course.chapter_set.all().count()
        has_fav_course = has_fav(request.user, data_id=course.id, fav_type=1)
        has_fav_teacher = has_fav(request.user, data_id=course.teacher_id, fav_type=2)
        relate_courses = get_relate_courses(course)
        if request.user.is_authenticated:
            has_learn = UserCourse.objects.filter(user=request.user, course=course).exists()
        else:
            has_learn = False
        
        return render(request, "course-detail.html", {
            "course": course,
            "chapter_num": chapter_num,
            "has_fav_course": has_fav_course,
            "has_fav_teacher": has_fav_teacher,
            "has_learn": has_learn,
            "relate_courses": relate_courses
        })
    

class CourseChapterView(LoginRequiredView, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        # 判断用户是否学习过该课程
        if not UserCourse.objects.filter(user=request.user, course=course).exists():
            new_user_course = UserCourse(user=request.user, course=course)
            new_user_course.save()
            course.learn_num += 1
            course.save()
        relate_courses = get_relate_courses(course)
        course_resources = CourseResource.objects.filter(course_id=course_id)
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "relate_courses": relate_courses
        })


class CourseCommentsView(LoginRequiredView, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        relate_courses = get_relate_courses(course)
        course_resources = CourseResource.objects.filter(course_id=course_id)
        comments = CourseComments.objects.filter(course_id=course_id).order_by('-create_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, per_page=10, request=request)
        page_comments = p.page(page)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "comments": page_comments,
            "relate_courses": relate_courses
        })
    
    def post(self, request,  course_id):
        if not request.user.is_authenticated:
            return HttpResponse(
                '{"status":"failed", "msg":"用户未登陆"}',
                content_type="application/json"
            )
        comment = request.POST.get("comment", '')
        if Course.objects.filter(id=course_id).exists() and comment:
            new_comment = CourseComments()
            new_comment.user = request.user
            new_comment.comment = comment
            new_comment.course_id = int(course_id)
            new_comment.save()
            return HttpResponse(
                '{"status":"successed"}',
                content_type="application/json"
            )
        else:
            return HttpResponse(
                '{"status":"failed", "msg":"提交了错误的数据"}',
                content_type="application/json"
            )
        

class VideoPlayView(LoginRequiredView, View):
    def get(self, request, video_id):
        current_content = request.GET.get("current_content", 'chapter')
        video = Video.objects.get(id=video_id)
        
        relate_courses = get_relate_courses(video.chapter.course)
        course_resources = CourseResource.objects.filter(course=video.chapter.course)
        comments = CourseComments.objects.filter(course_id=video.chapter.course_id).order_by('-create_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, per_page=10, request=request)
        page_comments = p.page(page)
        return render(request, "course-play.html", {
            "course": video.chapter.course,
            "current_video": video,
            "course_resources": course_resources,
            "relate_courses": relate_courses,
            "current_content": current_content,
            "comments": page_comments
        })