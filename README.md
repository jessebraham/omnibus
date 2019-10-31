# Omnibus

**Omnibus** is a simple web application for tracking comic book collections. It is built using [Django](https://www.djangoproject.com/) and backed by the [Goodreads API](https://www.goodreads.com/api/).

- - -

**Omnibus** is made possible by the following packages:  
[Django](https://github.com/django/django) | [django-webpack-loader](https://github.com/owais/django-webpack-loader) | [httpx](https://github.com/encode/httpx) | [Jinja2](https://github.com/pallets/jinja) | [marshmallow](https://github.com/marshmallow-code/marshmallow) | [xmltodict](https://github.com/martinblech/xmltodict)

- - -

## Quickstart

Begin by checking out the repository, creating and activating a virtual environment, and installing all dependencies:

```bash
$ # Check out repository and move into it
$ git clone https://github.com/jessebraham/omnibus.git
$ cd omnibus
# Create and activate a virtual environment, install requirements
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
# Install required NPM packages and build static assets
$ npm i && npm run dev
```

The `GOODREADS_API_KEY` and `GOODREADS_USER_ID` environment variables should be set prior to running the application. While the application will still load and function for the most part, the search and sync features will not work without these set.

More information regarding your API key can be found [in the Goodreads docs](https://www.goodreads.com/api/keys), and your User ID can be found by navidating to your Goodreads profile and extracting the numeric portion of the URL.

To set the variables:

```bash
$ export GOODREADS_API_KEY="[your-api-key]"
$ export GOODREADS_USER_ID="[your-user-id]"
```

Finally, perform the database migrations and run the application:

```bash
$ python manage.py migrate
$ python manage.py runserver
```

Navigate to `http://localhost:8000` in your browser to begin.

## Production

In order to run the application in production mode, a handful more environment variables are required. It's recommended that an `.env` file (which will be ignored by version control) is created in the project root directory containing the values for these variables. An simple template can be seen below:

```bash
export GOODREADS_API_KEY=""
export GOODREADS_USER_ID=""


# Instruct Django to load the production settings, rather than the
# default development settings. Be sure to set a strong secret key
# for Django.
export DJANGO_SETTINGS_MODULE="omnibus.settings.production"
export SECRET_KEY=""

# More information on DATABASE_URL formatting can be found at:
# https://github.com/jacobian/dj-database-url#url-schema
export DATABASE_URL=""

# ALLOWED_HOSTS should be a string containing either a single host or
# a comma-separated list of hosts. Defaults to 'localhost' if this
# variable is not set.
export ALLOWED_HOSTS=""
```

This environment variables can then be set by running `source .env` in a terminal.

Additionally, you should ensure that the CSS and JS have been built in production mode to minimize bundle size:

```bash
$ npm run prod
```

- - -

## To Do

- [ ] Write a reasonable amount of tests
- [ ] Add a method of displaying info/error messages
- [ ] Sync changes in a book's read status and/or rating back to Goodreads when updated
- [ ] Add some graphs and/or other interesting metrics to stats page
- [ ] Improve syncing speed (parallel requests?)
