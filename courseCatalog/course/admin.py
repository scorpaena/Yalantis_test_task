from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'start_date', 'end_date', 'number_of_lectures')
    list_filter = ('course_name', 'start_date', 'end_date', 'number_of_lectures')

admin.site.register(Course, CourseAdmin)
