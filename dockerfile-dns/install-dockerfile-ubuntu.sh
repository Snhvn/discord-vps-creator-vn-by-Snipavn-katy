cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt update
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt install -y tmate curl wget sudo systemctl neofetch procps systemd systemd-sysv dbus gnupg2 apt-transport-https ca-certificates software-properties-common net-tools dnsutils iputils-ping

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN systemctl enable docker

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
EOF
