FROM docker.io/node:24.3-bookworm-slim

WORKDIR /app

COPY ./package.json /app

RUN npm install && npm cache clean --force

ENV PATH=./node_modules/.bin/:$PATH
