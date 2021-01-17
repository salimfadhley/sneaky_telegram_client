FROM python:3.9-buster as py
RUN pip install --upgrade pip setuptools
COPY src/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY src src
WORKDIR /src
RUN pip install -e .
