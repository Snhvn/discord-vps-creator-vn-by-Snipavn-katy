cat <<EOF > Dockerfile4
FROM fedora

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf update -y 
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf dnf install tmate -y
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf install -y wget fastfetch curl git systemctl sudo

EOF
