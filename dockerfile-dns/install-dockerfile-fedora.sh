cat <<EOF > Dockerfile4
FROM fedora

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf update -y
RUN dnf install -y tmate curl wget sudo fastfetch procps systemd systemd-sysv dbus gnupg2 apt-transport-https ca-certificates software-properties-common net-tools dnsutils iputils-ping docker.io

RUN cd && echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && \
    curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN systemctl enable docker

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

EOF
