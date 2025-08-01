cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt update
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt install -y tmate
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt install -y curl wget sudo systemctl neofetch
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
