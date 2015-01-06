calendall
=========

Calendall is the next generation public calendar repository. You will be able
to explore, rate, export, import and share public calendars.

Callendall always will be open source.

Also this project is made with full stack development, this means:

    * Issues with kanban
    * Unit tests
    * Continous integration
    * Full automation
    * Different environments

So could be used as a project to learn from.

Status
======

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/calendall/calendall?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![CircleCI](https://circleci.com/gh/calendall/calendall.png?style=shield&circle-token=:circle-token)](https://circleci.com/gh/calendall/calendall)

[![Coverage Status](https://img.shields.io/coveralls/calendall/calendall.svg)](https://coveralls.io/r/calendall/calendall?branch=master)

[![Requirements Status](https://requires.io/github/calendall/calendall/requirements.svg?branch=master)](https://requires.io/github/calendall/calendall/requirements/?branch=master)

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

Execute the script to prepare de db with the user and password for the calendall DB:

    $ ./prepare_db.sh

Now apply migrations:

    $ fig run web ./manage.py migrate

Stop the containers:

    $ fig stop

Done!

Note: If you remove the `dbdata` container, you have to do this again

### After the first run

Just run:

    $ fig up -d


To gain control of the web app prompt (close and reload django dev server...)
the web service is stopped by default, you ned to run django webserver by hand,
this is handy for development, so.. just do:

    $ fig run --rm --service-ports web ./manage.py runserver 0.0.0.0:8000

Done! go to `127.0.0.1:8000`

Some people like to have full control like if they whee ssh running, if you are
thouse kind of people use:

    $ fig run --rm --service-ports web /bin/bash

####Note

> You need --service-ports implemented in fig, was added in [485 issue](https://github.com/docker/fig/pull/485)
> so, if the fig version you are using is < 1.1.0 you will need to install from
> the git repository

    pip install git+https://github.com/docker/fig.git

License
=======

See [LICENSE](https://github.com/calendall/calendall/blob/master/LICENSE)