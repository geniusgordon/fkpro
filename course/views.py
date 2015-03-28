from django.shortcuts import render
from course.models import * 
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from course.course_time import getCurrentCourse
from datetime import datetime, timedelta

import logging
import requests
import json

logger = logging.getLogger(__name__)
# Create your views here.
def test(request):
    c = CourseList.objects.all()[0].getCourseList()
    return HttpResponse(c[0][0])

@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, "course/login.html")
    if request.method == "POST":
        print "POST, %s %s" % \
                    (request.POST['username'], request.POST['password'])
        s, created = Student.objects.get_or_create(sid=request.POST['username'])
        c, created = CourseList.objects.get_or_create(student=s)
        if not created:
            c.parseCourse(request.POST['username'], request.POST['password'])
        return HttpResponse("success")

def getCourse(request, student, day=None, num=None):
    logger.info("GET COURSE, %s, %s, %s" % (student, day, num))
    try:
        s = Student.objects.get(sid=student)
        c = CourseList.objects.get(student=s)
    except Student.DoesNotExist:
        raise Http404("student not exists")
    except CourseList.DoesNotExist:
        raise Http404("course list not exists")
    course = c.getCourseList()
    if day is None and num is None:
        jsn = {"len": len(course), 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
        for n in range(len(course)):
            for d in range(len(course[n])):
                jsn[d+1][n+1] = course[n][d]
        return JsonResponse(jsn)
    if day is not None and num is None:
        jsn = {"len": len(course)}
        for n in range(len(course)):
            jsn[n+1] = course[n][int(day)-1]
        return JsonResponse(jsn)
    try:
        name = course[int(num)-1][int(day)-1]
        return HttpResponse(name)
    except:
        raise Http404("out of index, %s %s", day, num)

def getNow(request, student):
    try:
        s = Student.objects.get(sid=student)
    except Student.DoesNotExist:
        raise Http404("student not exists")
    now = (datetime.now() + timedelta(hours=8)).time()
    day = (datetime.now() + timedelta(hours=8)).weekday()
    course = getCurrentCourse(s, day+1, now)
    return JsonResponse(course)

@csrf_exempt
def gcm(request, student):
    try:
        s = Student.objects.get(sid=student)
    except Student.DoesNotExist:
        raise Http404("student not exists")
    if request.method == "POST":
        print request.POST["gcmid"]
        s.gcmid = request.POST["gcmid"]
        s.save()
        return HttpResponse("gcmid added")
    else:
        return HttpResponse(s.gcmid)

@csrf_exempt
def alarm(request):
    if request.method == "POST":
        cid = request.POST["course"]
        try:
            course = Course.objects.get(pk=cid)
            url = "https://android.googleapis.com/gcm/send"
            headers = {
                "Authorization": "key=AIzaSyAHCnGRHrMMIBypF0K8KjjCoCGicA5vI9Q",
                "Content-Type": "application/json;charset=UTF-8",
            }
            data = {"registration_ids": [], "data": {"course": course.name}}
            for s in course.student.all():
                data["registration_ids"].append(str(s.gcmid))
            r = requests.post(url, headers=headers, 
                          data=str(data).replace("'", "\"")
                              .replace("u\"", "\""))
            return HttpResponse("alarm")
        except Course.DoesNotExist:
            raise Http404("course not exists")
    else:
        return HttpResponse("not post")

