FROM node:16-buster-slim

WORKDIR /app

COPY ./package.json /app

RUN npm install && npm cache clean --force

ENV PATH ./node_modules/.bin/:$PATH
