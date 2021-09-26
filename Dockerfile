FROM python:3.8

WORKDIR /web
COPY . /web/
RUN pip install flask
RUN pip install geoip2
RUN pip install uwsgi

VOLUME /web/database
EXPOSE 8001

CMD ["uwsgi", "--ini", "app.ini"]
