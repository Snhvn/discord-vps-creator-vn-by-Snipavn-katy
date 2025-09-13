cat <<EOF > Dockerfile4
FROM fedora

RUN dnf update -y && \
    dnf install -y tmate curl wget sudo fastfetch procps systemd systemd-sysv docker.io

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN systemctl enable docker

STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

EOF
