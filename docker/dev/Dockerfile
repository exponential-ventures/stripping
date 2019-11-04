FROM k2so.xnv.io/numpy

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

LABEL version="0.1"
LABEL description="Stripping container"
LABEL maintainer="Adriano Marques <adriano@xnv.io>"


RUN apk add --no-cache --update \
    build-base gcc python python-dev

WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r  requirements.txt

COPY . /usr/src/app/

CMD /bin/bash