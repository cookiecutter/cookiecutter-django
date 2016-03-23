FROM {{ cookiecutter.repo_name|replace('_', '') }}_django

# Install OpenSSH
RUN apt-get update && \
    apt-get -y install openssh-server && \
    rm -rf /var/lib/apt/lists/*

# sshd needs this directory to run
RUN mkdir -p /var/run/sshd

# Copy configuration and entrypoint script
COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22
EXPOSE 8000

ENTRYPOINT ["/app/compose/debug/entrypoint.sh"]
