FROM postgres:{{ cookiecutter.postgresql_version }}

ADD ./compose/production/postgres/backup.sh /usr/local/bin/backup
ADD ./compose/production/postgres/restore.sh /usr/local/bin/restore
ADD ./compose/production/postgres/list-backups.sh /usr/local/bin/list-backups

RUN chmod +x /usr/local/bin/restore
RUN chmod +x /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/backup
