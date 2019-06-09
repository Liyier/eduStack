"""
author@liyi
date: 2019/5/26
"""
# from publisher.models import Publisher
# 
# 
# def update_course_num():
#     """可以通过定时任务的方式手动更新数据"""
#     publishers = Publisher.objects.all()
#     for publisher in publishers:
#         teachers = publisher.teacher_set.all()
#         course_num = 0
#         for teacher in teachers:
#             course_num += teacher.course_set.count()
#         publisher.course_num = course_num
#         publisher.save()
#         print("{}课程数已更新...".format(publisher.name))
# 
