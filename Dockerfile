FROM tozd/runit:ubuntu-xenial

EXPOSE 80/tcp
ENV DJANGO_SETTINGS_MODULE mainpage.settings_production

#Set secrets by uncommenting lines below
#ENV DB_PASSWORD ...
#Make this unique, and don't share it with anybody.
#ENV SECRET_KEY ...
#You can find them at: https://www.google.com/recaptcha/admin
#ENV RECAPTCHA_PUBLIC_KEY ...
#ENV RECAPTCHA_PRIVATE_KEY ...
#ENV PAYPAL_IDENTITY_TOKEN_PRODUCTION ...


# Update packages
RUN apt-get update -q -q && \
    apt-get install --no-install-recommends -y git python python-dev python-pip python-setuptools build-essential libgeoip-dev libpq-dev swig libxml2-dev libxslt1-dev subversion mercurial libaprutil1 apache2-dev

ADD ./requirements.txt /code/requirements.txt
ADD ./requirements-production.txt /code/requirements-production.txt

# Install Python package dependencies (do not use pip install -r here!)
RUN pip install --upgrade --force-reinstall pip six requests && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-production.txt /code/requirements.txt | xargs -n 1 sh -c 'CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install $0 || exit 255'

# Remove unneeded build-time dependencies
RUN apt-get purge python-dev build-essential -y && \
    apt-get autoremove -y && \
rm -f /code/packages.txt /code/requirements.txt

# Add the current version of the code (needed for production deployments)
WORKDIR /code
ADD . /code