FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf

{% if cookiecutter.use_certbot == 'y' and cookiecutter.use_docker == 'y' %}
COPY start.sh /start.sh
COPY nginx-secure.conf /etc/nginx/nginx-secure.conf
COPY dhparams.pem /etc/ssl/private/dhparams.pem
CMD /start.sh
{% endif %}
