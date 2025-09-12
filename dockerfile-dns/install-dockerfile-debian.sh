cat <<EOF > Dockerfile2
FROM debian:12

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt update
RUN apt install -y tmate curl wget sudo systemctl neofetch procps systemd systemd-sysv dbus gnupg2 apt-transport-https ca-certificates software-properties-common net-tools dnsutils iputils-ping

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
EOF
