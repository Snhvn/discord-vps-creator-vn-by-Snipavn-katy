cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
RUN apt update
RUN apt install -y tmate
RUN apt install -y curl wget sudo systemctl neofetch

EOF
