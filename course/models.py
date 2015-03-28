from django.db import models
import json
import parse

# Create your models here.
class Student(models.Model):
    sid = models.CharField(max_length=10)

    def __str__(self):
        return self.sid

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

    def __str__(self):
        return self.student.__str__()

