cat <<EOF > Dockerfile2
FROM debian:12

RUN apt update
RUN apt install -y tmate
RUN apt install -y curl wget sudo systemctl neofetch
RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
