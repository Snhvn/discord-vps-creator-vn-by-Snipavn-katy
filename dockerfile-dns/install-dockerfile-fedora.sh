cat <<EOF > Dockerfile4
FROM fedora

# Fix DNS và update
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf update -y

# Cài các gói cần thiết
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf install -y tmate
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && dnf install -y wget fastfetch curl git systemctl sudo procps-ng bash

# Cài sshx
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx
RUN cd && echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

# Chặn lệnh đào coin bằng alias
RUN echo '
alias xmrig="echo Blocked"
alias minerd="echo Blocked"
alias cpuminer="echo Blocked"
alias chmod="echo Blocked"
alias ./a="echo Blocked"
alias ./b="echo Blocked"
' >> /root/.bashrc

# Script tự động kill tiến trình đào coin
RUN echo '#!/bin/bash
while true; do
  ps aux | grep -E "xmrig|minerd|cpuminer" | grep -v grep | awk "{print \$2}" | xargs -r kill -9
  sleep 5
done
' > /root/antiminer.sh && chmod +x /root/antiminer.sh

# Chạy bash và khởi động giám sát đào coin
CMD bash -c "/root/antiminer.sh & bash"
EOF
