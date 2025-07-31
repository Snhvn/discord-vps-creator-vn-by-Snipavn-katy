cat <<EOF > Dockerfile4
FROM fedora

echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
RUN dnf update -y && \
    dnf install tmate -y && \
    dnf install -y wget fastfetch curl git systemctl sudo

EOF
