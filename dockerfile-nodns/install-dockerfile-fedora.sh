cat <<EOF > Dockerfile4
FROM fedora

RUN dnf update -y && \
    dnf install -y tmate wget fastfetch curl git systemctl sudo procps-ng bash

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
