import os

import dj_database_url

from .common import *


# Production settings
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts can be set via the OMNIBUS_ALLOWED environment variable. It is
# required that the variable is set to either a single host, or a comma-
# separated string of hosts.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# For more info see: https://github.com/jacobian/dj-database-url
DATABASES = {"default": dj_database_url.config()}


# WhiteNoise settings
# http://whitenoise.evans.io/en/stable/index.html

MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
