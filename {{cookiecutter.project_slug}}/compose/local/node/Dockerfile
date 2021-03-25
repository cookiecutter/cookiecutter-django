FROM node:10-stretch-slim

WORKDIR /app/frontend

COPY ./frontend/package.json ./frontend/package-lock.json ./

RUN npm install

ENV PATH ./node_modules/.bin/:$PATH
