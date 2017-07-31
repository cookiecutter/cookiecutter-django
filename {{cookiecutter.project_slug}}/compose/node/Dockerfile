FROM node:7.10-slim

RUN mkdir -p /app

COPY ./package.json /app

WORKDIR /app

RUN npm install && npm cache clean

ENV PATH ./node_modules/.bin/:$PATH
