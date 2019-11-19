FROM k2so.xnv.io/ml

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

LABEL version="0.1"
LABEL description="Stripping container"
LABEL maintainer="Adriano Marques <adriano@xnv.io>"


RUN apk add --no-cache --update build-base gcc python python-dev

WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/

# We need to override the DNS to be able to access our internal PyPi server.
# This must be done on a per-layer basis, the DNS config will not be maintained on the next layers
RUN echo "nameserver 10.7.21.1" > /etc/resolv.conf  && \
    echo "search xnv.io" >> /etc/resolv.conf && \
    pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

CMD /bin/bash