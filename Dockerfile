FROM python:3.7-slim

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y gcc curl ca-certificates bash gcc git


COPY . /usr/src/app/

WORKDIR /usr/src/app/
RUN echo "10.17.31.219	pypi.xnv.io" > /etc/hosts  &&  pip install  --trusted-host pypi.xnv.io --index-url http://pypi.xnv.io aurum
RUN python3 setup.py sdist && pip install .

CMD /bin/bash