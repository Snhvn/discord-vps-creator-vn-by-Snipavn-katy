cat <<EOF > Dockerfile4
FROM fedora
MAINTAINER http://fedoraproject.org/wiki/Cloud

RUN dnf update -y && \
    dnf install tmate -y && \
    dnf install -y wget fastfetch curl git systemctl sudo

    EOF
