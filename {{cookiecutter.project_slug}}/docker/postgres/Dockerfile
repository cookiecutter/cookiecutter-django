FROM postgres:{{ cookiecutter.postgresql_version }}

COPY ./scripts/ /usr/local/bin/scripts/
RUN find /usr/local/bin/scripts/ -type f -exec sed -i 's/\r//' {} \;
RUN chmod +x /usr/local/bin/scripts/*
RUN mv /usr/local/bin/scripts/* /usr/local/bin/ \
    && rmdir /usr/local/bin/scripts/
