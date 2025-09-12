cat <<EOF > Dockerfile2
FROM debian:12

RUN apt update && \
    apt install -y tmate curl wget sudo neofetch procps systemd systemd-sysv dbus gnupg2 apt-transport-https ca-certificates software-properties-common net-tools dnsutils iputils-ping docker.io

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN systemctl enable docker

STOPSIGNAL SIGRTMIN+3

EOF
