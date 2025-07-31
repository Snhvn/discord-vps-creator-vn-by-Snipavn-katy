cat <<EOF > Dockerfile2
FROM debian:12

echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
RUN apt update
RUN apt install -y tmate
RUN apt install -y curl wget sudo systemctl neofetch

EOF
