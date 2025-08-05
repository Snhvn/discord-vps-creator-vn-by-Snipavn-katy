cat <<EOF > Dockerfile4
FROM fedora

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf update -y
RUN dnf install -y tmate wget fastfetch curl git systemctl sudo procps-ng bash

RUN cd && echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && \
    curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
