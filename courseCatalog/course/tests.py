from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Course

today = date.today()
yesterday = today-timedelta(days=1)


class CourseTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.payload = {
            'course_name': 'course',
            'start_date': today,
            'end_date': today,
            'number_of_lectures': 5
        }
        self.client = Client()
        self.client_anonymous = Client() #anonymous user (will not be logged in)
        User.objects.create_superuser(username='user1', password='passw')
        self.client.login(username='user1', password='passw')
        self.course = Course.objects.create(**self.payload)

    def test_course_get(self):
        # checks the HTTP 200 status and amount of items=1 in queryset
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_course_get_anonymous_user(self):
        # checks the HTTP 200 status and amount of items=1 in queryset
        response = self.client_anonymous.get('/course/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_course_post(self):
        request = self.client.post(
            '/course/',
            data=self.payload,
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 201)

    def test_course_post_invalid_data(self):
        # because CharField(blank=False)
        self.payload['course_name'] = ''
        request = self.client.post(
            '/course/',
            data=self.payload,
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 400)

    def test_course_post_anonymous_user(self):
        # see https://github.com/encode/django-rest-framework/issues/5968
        # this is the reason why 403(Forbidden) instead of 401(UnAuthorized) 
        request = self.client_anonymous.post(
            '/course/',
            data=self.payload,
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 403)

    def test_courseDetail_get_anonymous_user(self):
        response = self.client_anonymous.get('/course/{}'.format(self.course.id))
        self.assertEqual(response.status_code, 200)

    def test_courseDetail_put(self):
        request = self.client.put(
            '/course/{}'.format(self.course.id),
            data=self.payload,
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 200)

    def test_courseDetail_put_invalid_data(self):
        # because CharField(blank=False)
        self.payload['course_name'] = ''
        request = self.client.put(
            '/course/{}'.format(self.course.id),
            data=self.payload,
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 400)

    def test_courseDetail_put_anonymous_user(self):
        request = self.client_anonymous.put(
            '/course/{}'.format(self.course.id),
            data=self.payload,
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 403)

    def test_courseDetail_patch_get(self):
        request = self.client.patch(
            '/course/{}'.format(self.course.id),
            data={'course_name': 'course1'},
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 200)
        response = self.client.get('/course/{}'.format(self.course.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['course_name'], 'course1')

    def test_courseDetail_patch_invalid_data(self):
        # because CharField(blank=False)
        request = self.client.patch(
            '/course/{}'.format(self.course.id),
            data={'course_name': ''},
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 400)

    def test_courseDetail_patch_anonymous_user(self):
        request = self.client_anonymous.patch(
            '/course/{}'.format(self.course.id),
            data={'course_name': ''},
            content_type='application/json',
        )
        self.assertEqual(request.status_code, 403)

    def test_courseDetail_delete(self):
        request = self.client.delete('/course/{}'.format(self.course.id))
        self.assertEqual(request.status_code, 204)

    def test_courseDetail_delete_anonymous_user(self):
        request = self.client_anonymous.delete('/course/{}'.format(self.course.id))
        self.assertEqual(request.status_code, 403)

    def test_courseDetail_get_404(self): 
        # only single course obj is created (id=1)
        # id=2 throws HTTP 404 status 
        response = self.client.get('/course/{}'.format(self.course.id + 1))
        self.assertEqual(response.status_code, 404)

    def test_course_model(self):
        course_fetched = Course.objects.get(course_name=self.course.course_name)
        self.assertEqual(course_fetched.start_date, self.course.start_date)
        self.assertEqual(course_fetched.end_date, self.course.end_date)
        self.assertEqual(course_fetched.number_of_lectures, self.course.number_of_lectures)
        self.assertTrue(isinstance(course_fetched, Course))

    def test_course_model_start_date_check(self):
        self.payload['start_date'] = yesterday
        with self.assertRaises(ValueError):
            Course.objects.create(**self.payload)

    def test_course_model_end_date_check(self):
        self.payload['end_date'] = yesterday
        with self.assertRaises(ValueError):
            Course.objects.create(**self.payload)
