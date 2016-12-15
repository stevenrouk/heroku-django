# heroku-django

A 'press play' script for setting up your Django environment and deploying it to Heroku.

All you have to do is ```source setup_django_heroku.sh YOUR-PROJECT-NAME YOUR-HEROKU-APP-NAME```, and then fill in your Django admin user details when prompted. _(This assumes that all necessary dependencies are installed. Read below before running the script.)_

---

## Before You Get Started

1) Make sure you have an account on [Heroku](https://www.heroku.com/).
2) This script has only been testing on Ubuntu 14.04. Let me know if you test it on something different.
3) I recommend installing the latest version of either Python 2.x or 3.x before you start.

### If you don't have pip...

```bash
sudo apt-get update
sudo apt-get install python-pip
```

### If you don't have virtualenv...

```bash
sudo apt-get update
sudo apt-get install python-virtualenv
```

### If you don't have git...

```bash
sudo apt-get update
sudo apt-get install git
git config --global user.email "you@example.com"
git config --global user.name "Steven Rouk"
```

### If you don't have Heroku-CLI...

```bash
sudo apt-get update
sudo apt-get install ruby-full
sudo add-apt-repository "deb https://cli-assets.heroku.com/branches/stable/apt ./"
curl -L https://cli-assets.heroku.com/apt/release.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install heroku
heroku login
```

---

## Running the Script

Alright, here we go!

```bash
git clone https://github.com/stevenrouk/heroku-django
source setup_django_heroku.sh YOUR-PROJECT-NAME YOUR-HEROKU-APP-NAME
```

Then just fill in your Django admin user details when prompted.

That's it.

---

Example.

```bash
source setup_django_heroku.sh mysite classy-penguin-91919
```

---

## Some Notes

- Heroku app name: The script attempts to create a Heroku app with whatever name you provide, but the app name must be unique on Heroku or the script will fail. Try to come up with a name that you think no one else will have used before.
- Virtualenv & git: This script will create and activate a virtual environment for you, as well as create a git repo and add all files that should be in version control to a first commit.

---

## Best Practices

Using this script also helps you follow some best practices, like:
- Keeping your SECRET_KEY out of version control,
- Having Debug=False in your production settings file, and a local_settings file with Debug=True, and
- Using a virtual environment.

These things are already accounted for when the script sets up your environment, so you don't have to worry about it.
