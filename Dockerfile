FROM python:3.7.3-slim

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y gcc curl ca-certificates bash gcc git

WORKDIR /usr/src/app/

COPY . /usr/src/app/

CMD /bin/bash