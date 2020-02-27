FROM python:3.7.3-slim

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y gcc curl ca-certificates bash gcc git

WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/

# We need to override the DNS to be able to access our internal PyPi server.
# This must be done on a per-layer basis, the DNS config will not be maintained on the next layers
RUN echo "nameserver 10.7.21.1" > /etc/resolv.conf  && \
    echo "search xnv.io" >> /etc/resolv.conf && \
    pip install --extra-index-url https://l337.xnv.io:443/ -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

CMD /bin/bash