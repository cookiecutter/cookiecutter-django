FROM {{ cookiecutter.repo_name|replace('_', '') }}_django

# Install setuptools, pip and OpenSSH
RUN \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python-pip python-setuptools python3-pip python3-setuptools openssh-server && \
    rm -rf /var/lib/apt/lists/*

# sshd needs this directory to run
RUN mkdir -p /var/run/sshd

# Copy configuration and entrypoint script
COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22
EXPOSE 8000

ENTRYPOINT ["/app/compose/debug/entrypoint.sh"]
