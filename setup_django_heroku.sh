# setup virtual environment and install dependencies
virtualenv venv
source venv/bin/activate
pip install django dj-database-url gunicorn whitenoise
pip freeze > requirements.txt

# start Django project
django-admin startproject "$1" .
python manage.py makemigrations
python manage.py migrate

# add necessary Heroku files and settings
python setup_django_heroku.py "$1"
python manage.py collectstatic --noinput

# create Django admin
printf "\n\n********************\nLet's create an admin user for you:\n\n"
python manage.py createsuperuser

# create git repo, add first commit
git init
git add -A
git commit -m "first commit"

# create Heroku app
heroku create "$2"

# set Heroku config vars from the .env file
while read line || [[ -n $line ]]; do heroku config:set $line; done < .env

# deploy!
heroku git:remote -a "$2"
git push heroku master
heroku run python manage.py migrate
heroku open
