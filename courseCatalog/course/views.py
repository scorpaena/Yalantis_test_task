from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer
from .filters import CourseFilter

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by('start_date')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = CourseFilter


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        obj = get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        return obj
