from datetime import time
from course.models import Course

course_time = [
    (time(8,0), time(9,0)),
    (time(9,0), time(10,0)),
    (time(10,0), time(11,0)),
    (time(11,0), time(12,0)),
    (time(12,0), time(13,0)),
    (time(13,0), time(14,0)),
    (time(14,0), time(15,0)),
    (time(15,0), time(16,0)),
    (time(16,0), time(17,0)),
    (time(17,0), time(18,0)),
    (time(18,0), time(19,0)),
    (time(19,0), time(20,0)),
    (time(20,0), time(21,0)),
    (time(21,0), time(22,0)),
]

def getCurrentCourse(student, day, now):
    day = 1
    now = time(8, 30)
    for t in range(len(course_time)):
        if course_time[t][0] <= now and now < course_time[t][1]:
            try:
                c = Course.objects.get(student=student, day=day, num=t+1)
                return {"name": c.name, "id": c.pk}
            except Course.DoesNotExist:
                return {"no": "class"}
    return {"no": "school"}

