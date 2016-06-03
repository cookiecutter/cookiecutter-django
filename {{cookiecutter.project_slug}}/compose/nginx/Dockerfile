FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf

{% if cookiecutter.use_certbot == 'y' and cookiecutter.use_docker == 'y' %}
ADD start.sh /start.sh
ADD nginx-secure.conf /etc/nginx/nginx-secure.conf
ADD dhparams.pem /etc/ssl/private/dhparams.pem
ADD /start.sh
{% endif %}
