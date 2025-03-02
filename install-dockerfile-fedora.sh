cat <<EOF > Dockerfile4
FROM fedora

RUN dnf update -y && \
    dnf install tmate -y && \
    dnf install -y wget fastfetch curl git systemctl sudo

EOF
