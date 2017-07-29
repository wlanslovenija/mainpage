FROM tozd/runit:ubuntu-xenial

EXPOSE 80/tcp
ENV DJANGO_SETTINGS_MODULE mainpage.settings_production

RUN apt-get update -q -q && \
    apt-get install --no-install-recommends -y git python python-dev python-pip python-setuptools build-essential libgeoip-dev libpq-dev swig libxml2-dev libxslt1-dev subversion mercurial libaprutil1 apache2-dev

ADD ./requirements.txt /code/requirements.txt
ADD ./requirements-production.txt /code/requirements-production.txt

# Install Python package dependencies
RUN pip install --upgrade --force-reinstall pip six requests && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-production.txt /code/requirements.txt | xargs -n 1 sh -c 'CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install $0 || exit 255'

WORKDIR /code
ADD . /code