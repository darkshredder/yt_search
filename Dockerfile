# pull official base image
FROM python:3.8.10-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apk add -u gcc musl-dev
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input --clear


# run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]