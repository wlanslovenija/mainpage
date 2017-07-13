FROM tozd/runit:ubuntu-xenial

EXPOSE 80/tcp
ENV DJANGO_SETTINGS_MODULE mainpage.settings

RUN apt-get update -q -q && \
    apt-get install --no-install-recommends -y git python python-dev python-pip python-setuptools build-essential libgeoip-dev libpq-dev swig libxml2-dev libxslt1-dev subversion mercurial libaprutil1 apache2-dev

ADD ./requirements.txt /code/requirements.txt
ADD ./requirements-production.txt /code/requirements-production.txt

# Install Python package dependencies
RUN pip install --upgrade --force-reinstall pip six requests && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-production.txt /code/requirements.txt | xargs -n 1 sh -c 'CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install $0 || exit 255'

RUN pip install --upgrade --force-reinstall -e svn+https://trac-hacks.org/svn/footnotemacro/trunk/#egg=FootNoteMacro
RUN pip install --upgrade --force-reinstall -e git+https://github.com/mitar/trac-mathjax.git@e5b2bcbd8ec74685407c6fb2e71fb56cc2f47484#egg=MathJaxPlugin-dev
RUN pip install --upgrade --force-reinstall -e svn+https://trac-hacks.org/svn/dashessyntaxplugin/0.11/#egg=TracDashesSyntaxPlugin
RUN pip install --upgrade --force-reinstall -e hg+https://bitbucket.org/kisielk/tracmathplugin#egg=TracMath-dev
RUN pip install --upgrade --force-reinstall -e git+https://github.com/herzbube/python-aprmd5.git#egg=python-aprmd5
RUN pip install --upgrade --force-reinstall -e git+https://github.com/wlanslovenija/cmsplugin-blog.git@0829d67e47934ab021206661ad5df7e7e1573b89#egg=cmsplugin_blog-dev
RUN pip install --upgrade --force-reinstall -e git+https://github.com/maccesch/cmsplugin-contact.git@ea95740655582faf603cb2f0f772f3600f952a6b#egg=cmsplugin_contact-dev
RUN pip install --upgrade --force-reinstall -e git+https://github.com/stefanfoulis/cmsplugin-filer.git@9f2e5959c25b849ba64d4a6be10d6ccd7278e050#egg=cmsplugin_filer-dev
RUN pip install --upgrade --force-reinstall -e git+https://github.com/mitar/django-cms.git@0bcf0409d5a052f136850cd03f6b54149a3983c5#egg=django_cms-dev
RUN pip install --upgrade --force-reinstall -e git+https://github.com/mitar/django-filer.git@d9917b1458c5abd41f47bc98c56d197d4ccd6fa0#egg=django_filer-dev
RUN pip install --upgrade --force-reinstall -e git+https://github.com/wlanslovenija/simple-translation.git@94c5e5639532411e070e9746c0ebd802e142b208#egg=simple_translation-dev