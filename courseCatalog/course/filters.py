from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    course_name = filters.CharFilter(lookup_expr='icontains')
    start_date = filters.DateFilter(lookup_expr='iexact')
    end_date = filters.DateFilter(lookup_expr='iexact')

    class Meta:
        model = Course
        fields = ['course_name','start_date', 'end_date']
