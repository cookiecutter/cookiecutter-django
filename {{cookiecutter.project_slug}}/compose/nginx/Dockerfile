FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf

{% if cookiecutter.use_lets_encrypt == 'y' and cookiecutter.use_docker == 'y' %}
# installs the `ps` command in the nginx image
RUN apt-get update && apt-get install -y procps

ADD start.sh /start.sh
ADD nginx-secure.conf /etc/nginx/nginx-secure.conf
ADD dhparams.pem /etc/ssl/private/dhparams.pem
CMD /start.sh
{% endif %}
