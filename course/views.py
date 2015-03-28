from django.shortcuts import render
from course.models import CourseList
from django.http import HttpResponse

# Create your views here.
def test(request):
    c = CourseList.objects.all()[0].getCourseList()
    return HttpResponse(c[0][0])

def getCourse(request, student, day, num):
    pass

