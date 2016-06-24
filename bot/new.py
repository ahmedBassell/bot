import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
    '/home/ahmed/django/bot/static/',
]

print STATICFILES_DIRS