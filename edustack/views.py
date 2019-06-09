from django.shortcuts import render
from django.views.generic import View
from course.models import Course
from publisher.models import Publisher
from users.models import Banner


class IndexView(View):
    def get(self, request):
        courses = Course.objects.all()[:8]
        banners = Banner.objects.all().order_by('index')
        publishers = Publisher.objects.all()[:10]
    
        return render(request, 'index.html', {
            "banners": banners,
            "courses": courses,
            "publishers": publishers
        })


