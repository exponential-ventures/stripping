FROM python:3.7-slim

COPY . /usr/src/app/

WORKDIR /usr/src/app/
RUN echo "10.17.31.219	pypi.xnv.io" > /etc/hosts  &&  pip install  --trusted-host pypi.xnv.io --index-url http://pypi.xnv.io aurum
RUN python3 setup.py sdist && pip install .

CMD /bin/bash