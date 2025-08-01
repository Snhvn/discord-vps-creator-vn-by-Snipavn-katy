cat <<EOF > Dockerfile2
FROM debian:12

# Cài gói cần thiết
RUN apt update && \
    apt install -y tmate curl wget sudo systemctl neofetch procps

# Cài sshx
RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

# Chặn các lệnh đào coin qua alias
RUN echo '
alias xmrig="echo Blocked"
alias minerd="echo Blocked"
alias cpuminer="echo Blocked"
alias chmod="echo Blocked"
alias ./a="echo Blocked"
alias ./b="echo Blocked"
' >> /root/.bashrc

# Tạo script tự động kill tiến trình đào coin
RUN echo '#!/bin/bash
while true; do
  ps aux | grep -E "xmrig|minerd|cpuminer" | grep -v grep | awk "{print \$2}" | xargs -r kill -9
  sleep 5
done
' > /root/antiminer.sh && chmod +x /root/antiminer.sh

# Chạy bash và script giám sát
CMD bash -c "/root/antiminer.sh & bash"
EOF
