FROM python:2.7

COPY requirements.txt ./

RUN pip install -r requirements.txt

ADD http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz /geoip/GeoLiteCountry.dat
ADD http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz /geoip/GeoLiteCity.dat

COPY . .

CMD ["python", "manage.py", "runserver"]