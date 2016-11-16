import os
import platform
import re
import sys

PROJECT_NAME = sys.argv[1]

# create .gitignore
with open('.gitignore', 'w') as f:
    f.write("""venv
*.pyc
__pycache__
db.sqlite3
static
.env
""")


# add psycopg2 to requirements
with open('requirements.txt', 'a') as f:
    f.write('\npsycopg2==2.5.4\n')


# write Procfile
with open('Procfile', 'w') as f:
    f.write("web: gunicorn {}.wsgi".format(PROJECT_NAME))


# write runtime.txt
with open('runtime.txt', 'w') as f:
    python_version = platform.python_version()
    f.write('python-{}'.format(python_version))


# write local_settings file
with open(os.path.join(PROJECT_NAME, 'local_settings.py'), 'w') as f:
    f.write("""import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
""")


# remove 'debug=True' from settings
with open(os.path.join(PROJECT_NAME, 'settings.py'), 'r') as f:
    file = f.read()
file = file.replace("# SECURITY WARNING: don't run with debug turned on in production!", "")
file = file.replace("DEBUG = True", "")
with open(os.path.join(PROJECT_NAME, 'settings.py'), 'w') as f:
    f.write(file)


# move secret key to secret_settings.py file
with open(os.path.join(PROJECT_NAME, 'settings.py'), 'r') as f:
    file = f.read()
SECRET_KEY = re.findall('SECRET_KEY = (.+)\n', file)[0]
file = file.replace(SECRET_KEY, "os.environ['SECRET_KEY']")
with open(os.path.join(PROJECT_NAME, 'settings.py'), 'w') as f:
    f.write(file)
with open(os.path.join('.env'), 'w') as f:
    f.write("SECRET_KEY={}".format(SECRET_KEY))
with open(os.path.join('.env.template'), 'w') as f:
    f.write("SECRET_KEY='my-secret-key'")


# append to settings file
with open(os.path.join(PROJECT_NAME, 'settings.py'), 'r') as f:
    file = f.read()
if "DATABASES['default'] = dj_database_url.config()" not in file:
    with open(os.path.join(PROJECT_NAME, 'settings.py'), 'a') as f:
        f.write("""

# Set static path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# Database settings
import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = False

try:
    from .local_settings import *
except ImportError:
    pass
""")


# write wsgi file
with open(os.path.join(PROJECT_NAME, 'wsgi.py'), 'r') as f:
    file = f.read()
if "application = DjangoWhiteNoise(application)" not in file:
    with open(os.path.join(PROJECT_NAME, 'wsgi.py'), 'a') as f:
        f.write("\n\nfrom whitenoise.django import DjangoWhiteNoise\napplication = DjangoWhiteNoise(application)\n")


# write manage.py file that reads environment variables from .env
with open('manage.py', 'w') as f:
    f.write("""#!/usr/bin/env python
import os
import sys
import re


def read_env():
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings")

    from django.core.management import execute_from_command_line

    read_env()
    execute_from_command_line(sys.argv)
""".format(PROJECT_NAME))
