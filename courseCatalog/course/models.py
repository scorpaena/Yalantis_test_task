from django.db import models
from datetime import date

class Course(models.Model):
    course_name = models.CharField(max_length = 100)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    number_of_lectures = models.PositiveIntegerField(default=1)
    
    def clean(self):
        if self.start_date < date.today():
            raise ValueError('you cannot create courses in the past')
        elif self.start_date > self.end_date:
            raise ValueError("'end_date' cannot be before 'start_date'")

    def save(self, **kwargs):
        self.clean()
        return super().save(**kwargs)
    
    def __str__(self):
        return self.course_name
