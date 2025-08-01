cat <<EOF > Dockerfile4
FROM fedora

RUN dnf update -y 
RUN dnf install tmate -y
RUN dnf install -y wget fastfetch curl git systemctl sudo
RUN curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx
RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

EOF
