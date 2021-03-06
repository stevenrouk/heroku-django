# check that the arg for the Django project name was passed
if [ -z "$1" ]
then
echo "missing Django project name argument"
return 1
fi

# check that the arg for the Django project name is a valid all-lowercase alpha string
if ! [[ "$1" =~ ^[a-z]+$ ]]
then
echo "error: make sure your Django project name is only lowercase letters (no numbers or other characters)"
return 1
fi

# check that the arg for the Heroku app name is a valid string of alphanum separated by single hyphens
if ! [[ "$2" =~ ^([a-z0-9]+[\-]{0,1}[a-z0-9]+)+$ ]]
then
echo "error: make sure your Heroku app name is only lowercase alphanum separated by single hyphens"
return 1
fi

# remove heroku-django git repo and README.md to prepare for project's git repo
sudo rm -r .git
rm README.md

# setup virtual environment and install dependencies
virtualenv venv && source venv/bin/activate
pip install django dj-database-url gunicorn whitenoise
pip freeze > requirements.txt

# create the Django project
django-admin startproject "$1" .
# check if there was an error starting the Django project
if [ $? != 0 ]
then
echo "error creating the Django project"
return 1
fi

# apply migrations
python manage.py makemigrations && python manage.py migrate

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

