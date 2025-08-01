cat <<EOF > Dockerfile2
FROM debian:12

# Đảm bảo DNS hoạt động và cài đặt gói cần thiết
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt update
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt install -y tmate
RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && apt install -y curl wget sudo systemctl neofetch procps

# Cài sshx
RUN cd && echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

# Alias chặn lệnh đào coin
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

# Khởi chạy bash cùng script giám sát
CMD bash -c "/root/antiminer.sh & bash"
EOF
