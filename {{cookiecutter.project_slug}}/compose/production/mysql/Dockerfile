FROM mysql:{{ cookiecutter.database_version.lower().split('@')[1] }}

COPY ./compose/production/mysql/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

COPY ./compose/production/mysql/init.sh /docker-entrypoint-initdb.d
RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/init.sh
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/init.sh
