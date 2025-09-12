cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN apt update && \
    apt install -y tmate curl wget sudo systemctl neofetch procps systemd systemd-sysv dbus gnupg2 apt-transport-https ca-certificates software-properties-common net-tools dnsutils iputils-ping docker.io

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN systemctl enable docker

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

EOF
