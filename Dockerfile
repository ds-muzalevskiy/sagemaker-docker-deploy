FROM ubuntu:20.04

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3.8 \         
         ca-certificates \
	 python3-pip \
	 python3-setuptools \
	 python3-numpy \
         python3-scipy \
         python3-pandas \
	 python3-sklearn \
	 nginx \
	 python3-flask \
	 python3-gevent \
         gunicorn \
	 python-is-python3


ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY decision_trees /opt/program
WORKDIR /opt/program
