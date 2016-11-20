# heroku-django

A 'press play' script for setting up your Django environment and deploying it to Heroku.

All you have to do is ```source setup_django_heroku.sh YOUR-PROJECT-NAME YOUR-HEROKU-APP-NAME```, and then fill in your Django admin user details when prompted.

That's it.

_(Note: This script does assume that you have Python, pip, virtualenv, and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line) installed. The script has only been tested in an Ubuntu 14.04 environment.)_

_(Another Note: This script will create and activate a virtual environment for you, as well as create a git repo and add all files that should be in version control to a first commit.)

---

Example.

```bash
source setup_django_heroku.sh mysite classy-penguin-91919
```

---

## Best Practices

Using this script also helps you follow some best practices, like:
- Keeping your SECRET_KEY out of version control,
- Having Debug=False in your production settings file, and a local_settings file with Debug=True, and
- Using a virtual environment.

These things are already accounted for when the script sets up your environment, so you don't have to worry about it.
