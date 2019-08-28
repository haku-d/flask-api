FROM python:3.7-alpine3.9

MAINTAINER thanh <thanh@clgt.vn>

RUN apk update && apk add tzdata &&\
    cp /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime &&\
    echo "Asia/Ho_Chi_Minh" > /etc/timezone &&\
    apk del tzdata && rm -rf /var/cache/apk/*

COPY requirements.txt requirements.txt
RUN apk add --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    && pip install --upgrade pip \
    && pip install gunicorn \
    && pip install gunicorn[gevent] \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

ENV APP_DIR /app
ENV FLASK_APP app
ENV FLASK_ENV production
ENV FLASK_DEBUG 0

# app dir
VOLUME [${APP_DIR}]
WORKDIR ${APP_DIR}

COPY . .

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 5000

RUN chmod a+x ./docker-entrypoint.sh

# exectute start up script
ENTRYPOINT ["./docker-entrypoint.sh"]

