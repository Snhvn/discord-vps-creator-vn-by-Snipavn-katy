cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN apt update
RUN apt install -y tmate
RUN apt install -y wget
RUN wget -O ngrok.tgz "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz" && \
tar -xf ngrok.tgz && \
rm -rf ngrok.tgz 
EOF
