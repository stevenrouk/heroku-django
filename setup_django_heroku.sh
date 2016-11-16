# setup virtual environment and install dependencies
virtualenv venv
source venv/bin/activate
pip install django dj-database-url gunicorn whitenoise
pip freeze > requirements.txt

# start Django project
django-admin startproject "$1" .
python manage.py makemigrations
python manage.py migrate

# create Django admin
printf "\n\n********************\nLet's create an admin user for you:"
python manage.py createsuperuser

# add necessary Heroku files and settings
python setup_django_heroku.py "$1"
python manage.py collectstatic

# create git repo, add first commit
git init
git add -A
git commit -m "first commit"

# create Heroku app
heroku create "$2"
heroku git:remote -a "$2"

# deploy!
git push heroku master
heroku run python manage.py migrate
heroku open
