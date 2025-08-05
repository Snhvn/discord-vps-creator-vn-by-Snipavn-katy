cat <<EOF > Dockerfile2
FROM debian:12

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt update
RUN apt install -y tmate curl wget sudo systemctl neofetch procps

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
