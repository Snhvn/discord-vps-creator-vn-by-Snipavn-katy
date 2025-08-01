cat <<EOF > Dockerfile1
FROM ubuntu:22.04

RUN apt update && \
    apt install -y tmate curl wget sudo systemctl neofetch procps

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
