from django.db import models
import json
import parse

# Create your models here.
class Student(models.Model):
    sid = models.CharField(max_length=10)
    gcmid = models.CharField(max_length=150)

    def __unicode__(self):
        return self.sid

class Course(models.Model):
    name = models.CharField(max_length=100)
    student = models.ManyToManyField(Student)
    day = models.IntegerField()
    num = models.IntegerField()

    def __unicode__(self):
        return self.name

class CourseList(models.Model):
    student = models.ForeignKey(Student)
    data = models.CharField(max_length=5000)

    def getCourseList(self):
        return json.loads(self.data)

    def parseCourse(self, username, password):
        s, created = Student.objects.get_or_create(sid=username)
        self.data = parse.parse(username, password)
        self.student = s
        self.save()
        c = self.getCourseList()
        for n in range(len(c)):
            for d in range(len(c[n])):
                if c[n][d].strip() != "":
                    course, created = \
                        Course.objects.get_or_create(name=c[n][d], 
                                                     day=d+1, num=n+1)
                    course.student.add(s)
                    course.save()

    def __unicode__(self):
        return self.student.__unicode__()

