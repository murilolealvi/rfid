FROM ubuntu:jammy

RUN apt-get update \
 && apt-get install -y wget gnupg \
 && wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - \
 && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list \
 && apt-get update \
 && apt-get install -y mongodb-org \
 && rm -rf /var/lib/apt/lists/*

COPY mongod.conf /etc/mongod.conf

EXPOSE 27017

VOLUME /var/log/mongodb
VOLUME /var/lib/mongo

CMD mongod --config /etc/mongod.conf
