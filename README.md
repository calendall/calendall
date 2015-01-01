calendall
=========

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/calendall/calendall?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![CircleCI](https://circleci.com/gh/calendall/calendall.png?circle-token=:circle-token)](https://circleci.com/gh/calendall/calendall)

Calendall stack
---------------

- Python 3.4.2
- Django 1.7.1
- Postgresql 9.4

Run in development
------------------

Calendall runs on top of Docker, in development and will run in production too,
so to run Calendall you just need the stack (see above). We will use 3 containers
one for the database data, one for the postgresql database and another with the
running application

These are the images:

- [slok/postgresql:1.0](https://github.com/slok/docker-postgresql)
- [slok/calendall:dev](https://github.com/slok/docker-calendall)

To glue all this stuff we will use [Fig](http://www.fig.sh/)

### First run

To create the users first we need to run the postgres database, so we will use fig:

    $ fig up -d

Web app will fail, no worries :)

Enter in the database:

    $ docker run --rm -it --link calendall_db_1:db slok/postgresql:1.0 /bin/bash

Once inside the container, connect to the database (default container user/pass is docker/docker):

    # psql -h $DB_PORT_5432_TCP_ADDR -U docker

And Create the database and user for the app:

    # CREATE USER calendall WITH PASSWORD 'calendall';
    # CREATE DATABASE calendall WITH OWNER calendall ENCODING 'UTF8';
    # GRANT ALL PRIVILEGES ON DATABASE "calendall" to calendall;
    # \q

We close the connection and we'll run the migrations:

    $ fig run web ./manage.py migrate

Stop the containers:

    $ fig stop

Done!

Note: If you remove the `dbdata` container, you have to do this again

### After the first run

Just run:

    $ fig up -d

Done! go to `127.0.0.1:8000`

If you want to gain control of the web app prompt (close and reload django dev server...):

    $ fig stop web
    $ fig run web

### Extra

As an extra stuff, you can rerun the app container to migrate database and stuff
like that.

Imagine that our app is running after doing `fig up -d`:

    $ fig ps
           Name                     Command               State            Ports
    -------------------------------------------------------------------------------------
    calendall_db_1       run                              Up       5432/tcp
    calendall_dbdata_1   true                             Exit 0
    calendall_web_1      python /code/calendall/man ...   Up       0.0.0.0:8000->8000/tcp

stop the `web` (calendall_web_1) container and run the migration:

    $ fig kill web
    $ fig run web calendall/manage.py migrate

And re run

    $ fig run web

