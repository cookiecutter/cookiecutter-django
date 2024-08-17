FROM docker.angie.software/angie:minimal
RUN rm /etc/angie/angie.conf && apk add --no-cache angie-console-light
COPY ./compose/production/angie/default.conf /etc/angie/angie.conf

CMD ["angie", "-g", "daemon off;"]
