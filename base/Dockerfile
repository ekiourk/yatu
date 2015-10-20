FROM debian:jessie
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
    python3.4 \
    python3-pip \
    python3-psycopg2 \
    libpq-dev

RUN apt-get remove -y python3-pip
RUN easy_install3 pip

# install requirements first to improve caching
RUN easy_install3 -U setuptools
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt


ADD . /opt/yatu/

# Create logs dir
RUN mkdir /var/log/yatu

# Install our python packages
RUN (cd /opt/yatu/ && \
    python3 setup.py install)