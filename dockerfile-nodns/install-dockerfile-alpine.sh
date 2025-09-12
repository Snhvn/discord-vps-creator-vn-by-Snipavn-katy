cat <<EOF > Dockerfile3
FROM alpine:3.19

RUN apk update && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add --no-cache tmate curl wget neofetch openrc docker
    
RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN rc-update add docker default

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

EOF
