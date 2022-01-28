#!/bin/bash


initialize() {
    {
        mysql_note "Giving user ${MYSQL_USER} access to schema test_${MYSQL_DATABASE}"
        docker_process_sql --database=mysql <<<"GRANT ALL ON \`test_${MYSQL_DATABASE//_/\\_}\`.* TO '$MYSQL_USER'@'%' ;"

        # exporting dummy MYSQL_ONETIME_PASSWORD to avoid -> MYSQL_ONETIME_PASSWORD: unbound variable
        export DUMMY_ONETIME_PASSWORD="$MYSQL_ROOT_PASSWORD"
    } || {
        exit 1
    }
}

docker_process_sql() {
	if [ -n "$MYSQL_DATABASE" ]; then
		set -- --database="$MYSQL_DATABASE" "$@"
	fi

	mysql --protocol=socket -uroot --password="${MYSQL_ROOT_PASSWORD}" -hlocalhost --socket="${SOCKET}" --comments "$@"
}

# logging functions
mysql_log() {
	local type="$1"; shift
	# accept argument string or stdin
	local text="$*"; if [ "$#" -eq 0 ]; then text="$(cat)"; fi
	local dt; dt="$(date --rfc-3339=seconds)"
	printf '%s [%s] [Entrypoint]: %s\n' "$dt" "$type" "$text"
}

mysql_note() {
	mysql_log Note "$@"
}

until (initialize); do
    >&2 echo 'Waiting for MYSQL to execute init'
    sleep 1
done
