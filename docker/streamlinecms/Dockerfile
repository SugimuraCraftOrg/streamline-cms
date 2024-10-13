FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Upgrade base packages.
RUN apt update \
    && apt upgrade -y \
    && pip install --upgrade pip

# Setup application.
# - directories.
RUN mkdir -p /opt/streamlinecms
RUN mkdir -p /var/streamlinecms
# - packages
RUN apt install -y postgresql-client \
    && apt clean
# - python
RUN mkdir -p /opt/streamlinecms
COPY .env /opt/streamlinecms/.env
WORKDIR /opt/streamlinecms
COPY ./streamlinecms/requirements.lock /opt/streamlinecms/requirements.lock
RUN pip install -r requirements.lock \
    && rm -rf ~/.cache/pip
# COPY ./streamlinecms/requirements.txt /opt/streamlinecms/requirements.txt
# RUN pip install -r requirements.txt \
#     && rm -rf ~/.cache/pip
# - startup
# CMD python
