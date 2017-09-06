FROM postgres:{{ cookiecutter.postgresql_version }}

COPY ./compose/production/postgres/backup.sh /usr/local/bin/backup
RUN chmod +x /usr/local/bin/backup

COPY ./compose/production/postgres/restore.sh /usr/local/bin/restore
RUN chmod +x /usr/local/bin/restore

COPY ./compose/production/postgres/list-backups.sh /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/list-backups
