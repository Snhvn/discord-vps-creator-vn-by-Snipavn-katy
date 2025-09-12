cat <<EOF > Dockerfile3
FROM alpine:3.19

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf

RUN apk update && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add --no-cache tmate curl wget sudo systemctl neofetch procps systemd systemd-sysv dbus gnupg2 apt-transport-https ca-certificates software-properties-common net-tools dnsutils iputils-ping
    


RUN cd && echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && \
    curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

EOF
