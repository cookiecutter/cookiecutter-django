FROM traefik:v2.0
RUN mkdir -p /etc/traefik/acme
RUN touch /etc/traefik/acme/acme.json
RUN chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik

RUN addgroup -g 101 -S traefik
RUN adduser -S -D -H -u 101 -s /sbin/nologin -G traefik -g traefik traefik
RUN chown -R traefik /etc/traefik

USER traefik
EXPOSE 8080/tcp 8443/tcp
