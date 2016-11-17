# heroku-django

A 'press play' script for setting up your Django environment and deploying it to Heroku.

All you have to do is ```source setup_django_heroku.sh YOUR-PROJECT-NAME YOUR-HEROKU-APP-NAME```, and then fill in your Django admin user details when prompted.

That's it.

---

Example.

```bash
source setup_django_heroku.sh mysite classy-penguin-91919
```

---

## Best Practices

Using this script also helps you follow some best practices, like keeping your SECRET_KEY out of version control, keeping a local_settings file with Debug=True so that your production settings can turn it off, etc.

These things are already accounted for when the script sets up your environment, so you don't have to worry about it.
