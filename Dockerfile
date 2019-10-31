FROM python:3.8.0-alpine

ENV LANG C.UTF-8

LABEL version="0.1"
LABEL description="Stripping container"
LABEL maintainer="Adriano Marques <adriano@xnv.io>"


    # --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
RUN apk add --no-cache --update \
    build-base gcc python python-dev \
    py-pip build-base py-numpy py-numpy-dev

WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r  requirements.txt