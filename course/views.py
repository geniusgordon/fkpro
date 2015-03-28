from django.shortcuts import render
from course.models import * 
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def test(request):
    c = CourseList.objects.all()[0].getCourseList()
    return HttpResponse(c[0][0])

@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, "course/login.html")
    if request.method == "POST":
        print "POST, %s %s" % (request.POST['username'], request.POST['password'])
        s, created = Student.objects.get_or_create(sid=request.POST['username'])
        c, created = CourseList.objects.get_or_create(student=s)
        if not created:
            c.parseCourse(request.POST['username'], request.POST['password'])
        return HttpResponse("success")

def getCourse(request, student, day, num):
    try:
        s = Student.objects.get(sid=student)
    except Student.DoesNotExist:
        raise Http404("student not exists")
    c = CourseList.objects.get(student=s).getCourseList()
    try:
        name = c[int(num)-1][int(day)-1]
        return HttpResponse(name)
    except:
        raise Http404("out of index, %s %s", day, num)

