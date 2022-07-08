FROM node:18-bullseye-slim

RUN apt-get update && apt-get install -y python3 g++ make

WORKDIR /app

COPY ./package.json /app

RUN npm install && npm cache clean --force

ENV PATH ./node_modules/.bin/:$PATH
