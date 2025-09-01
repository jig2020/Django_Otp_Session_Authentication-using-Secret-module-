from django.db import models
from django.utils import timezone
import datetime

class AllCourses(models.Model):
    coursename= models.CharField(max_length=200)
    instructorsname= models.CharField(max_length=100)
    courseprice= models.IntegerField()
    courseimage= models.ImageField(upload_to='images/')
    startedfrom= models.DateTimeField('Started From')
    def __str__(self):
        return self.coursename
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.startedfrom <= now


class CourseDetails(models.Model):
    couse= models.ForeignKey(AllCourses, on_delete=models.CASCADE)
    # selfpace= models.CharField(max_length=500)
    # instructorlead= models.CharField(max_length=500)
    coursetype=models.CharField(max_length=500)
    your_choice= models.BooleanField(default=False)
    def __str__(self):
        return str(self.coursetype)