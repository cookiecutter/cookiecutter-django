FROM traefik:2.3

WORKDIR /etc/traefik/

RUN addgroup --system traefik \
  && adduser \
  --disabled-password \
  --gecos '' \
  --no-create-home \
  --ingroup traefik \
  traefik \
  && mkdir acme/ \
  && touch acme/acme.json \
  && chmod 0600 acme/acme.json \
  && chown -R traefik:traefik .

EXPOSE 8080/tcp 8443/tcp

VOLUME /etc/traefik/acme/

USER traefik
