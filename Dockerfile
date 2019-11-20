FROM python:3.8-alpine
MAINTAINER Jesse Braham

# Do not write out .pyc files when importing source modules.
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
ENV PYTHONDONTWRITEBYTECODE 1

# Force stdin, stdout and stderr to be totally unbuffered.
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED 1

# Update Alpine package cache and install required system packages.
# This configuration assumes that PostgreSQL is being used. If you are using
# a different database, update the packages accordingly.
RUN apk update && apk add gcc musl-dev nodejs nodejs-npm postgresql-dev python3-dev

# Create a directory to hold the application and copy the project files from
# the local filesystem to said directory. Set the project directory as the
# working directory.
RUN mkdir -p ./opt/omnibus/
COPY . /opt/omnibus/
WORKDIR /opt/omnibus

# Install the Python requirements for production. Make sure to review (and
# modify if necessary) the packages in this file.
RUN pip install --no-cache-dir -r requirements.prod.txt

# Install the required packages and build the static assets for the project.
# Clean up when finished.
RUN npm install && npm run prod
RUN rm -rf node_modules

# Collect all static files.
RUN python manage.py collectstatic

# Specify the entrypoint script, which takes care of launching the application.
ENTRYPOINT ["sh", "/opt/omnibus/docker-entrypoint.sh"]
