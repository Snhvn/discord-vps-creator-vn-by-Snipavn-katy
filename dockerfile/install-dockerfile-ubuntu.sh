cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN apt update
RUN apt install -y tmate
RUN apt install -y curl wget sudo systemctl neofetch

EOF
