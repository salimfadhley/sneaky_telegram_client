FROM python:3.9-buster as py
RUN pip install --upgrade pip==21.0.1 setuptools
COPY src/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY src src
WORKDIR /src
RUN cat ./src/sneaky_client/_version.py
RUN pip install -e .

FROM nginx as sneaky_nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/
COPY ./nginx/index.html /usr/share/nginx/html/

FROM docker.elastic.co/elasticsearch/elasticsearch:7.10.2 as sneaky_elastic
