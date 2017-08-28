Mainpage
========

This is a repository for wlan-si web-page docker, it contains:

-  Web container for: django, uwgsi, nginx
-  Database container with postgresql

Installation
------------

Mainpage requires `docker <https://www.docker.com/>`__ and
`docker-compose <https://docs.docker.com/compose/>`__ to run.

Download the repository to disk and run docker-compose build.

.. code:: sh

    git clone https://github.com/wlanslovenija/mainpage
    cd mainpage
    docker-compose build

Then just run the docker-compose up, which will set up the database
create media and static folders, merge the database, and bring up the
production server for mainpage.

.. code:: sh

    docker-compose up

About
-----

This repository was a big part of my 2017 Gsoc project, it was suppose
to revive the unmaintained repository of wlan-si.net web-page, which had
a lot of broken dependencies, outdated dependencies and was not yet
running inside of a docker container.

I managed to successfully create docker containers for both website and
database but my lack of django knowledge left me short of actually
fixing the django project that was suppose to run.

Future
------

All that is left is for someone to fix the broken django project-