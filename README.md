# Omnibus

**Omnibus** is a simple web application for tracking comic book collections. It is built using [Django](https://www.djangoproject.com/) and backed by the [Goodreads API](https://www.goodreads.com/api/).

- - -

**Omnibus** is made possible by the following packages:  
[Django](https://github.com/django/django) | [django-webpack-loader](https://github.com/owais/django-webpack-loader) | [httpx](https://github.com/encode/httpx) | [Jinja2](https://github.com/pallets/jinja) | [marshmallow](https://github.com/marshmallow-code/marshmallow) | [xmltodict](https://github.com/martinblech/xmltodict)

- - -

## Quickstart

Ensure that the `GOODREADS_API_KEY` and `GOODREADS_USER_ID` environment variables are set prior to running the application. More information regarding your API key can be found [here](https://www.goodreads.com/api/keys), and your User ID can be found by navidating to your Goodreads profile and extracting the numeric portion of the URL.

Begin by checking out the repository, creating and activating a virtual environment, and installing the required packages.

```bash
$ # Check out repository and move into it
$ git clone https://github.com/jessebraham/omnibus.git
$ cd omnibus
# Create and activate a virtual environment, install requirements
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
# Install required NPM packages and build static assets
$ npm i
$ npm run prod
```

Finally, perform the database migrations and run the application:

```bash
$ python manage.py migrate
$ python manage.py runserver
```

Navigate to `http://localhost:8000` in your browser to begin.
