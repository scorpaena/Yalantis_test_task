Abstract
--------
This is a test task for Yalantis Python School.
It is made using Django/DRF framework and represents simple catalog of courses, where the authorized users can create/read/update/delete items of courses.
For data storage the Python standard SQLite database is used.

Requirements
------------
1. Make sure to install all the required modules (see file 'requirements.txt'):
    `pip install -r requirements.txt`
2. Perform migration:
    `python manage.py migrate`

Instructions
------------
1. Create superuser:
    `python manage.py createsuperuser`
2. Run the server:
    `python manage.py runserver`
3. Go to http://127.0.0.1:8000/course/ in your web browser, login using 'username' and 'password', created at the step 1.
4. Once you are logged in, you can add new course item (Note: 'course_name' is mandatory for filling in; other fields have default values: 'start_date' = today, 'end_date' = today, 'number_of_lectures' = 1.
5. Click GET button to watch the result.
6. For navigation/search use 'Filters' button.
7. Go to http://127.0.0.1:8000/course/<int:course_id> to read/update/delete the course item using GET/PATCH/DELETE methods respectively.


