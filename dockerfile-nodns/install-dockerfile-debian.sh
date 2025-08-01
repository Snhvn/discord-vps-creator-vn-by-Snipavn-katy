cat <<EOF > Dockerfile2
FROM debian:12

RUN apt update && \
    apt install -y tmate curl wget sudo systemctl neofetch procps

RUN curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN echo '
alias xmrig="echo Blocked"
alias minerd="echo Blocked"
alias cpuminer="echo Blocked"
alias chmod="echo Blocked"
alias ./a="echo Blocked"
alias ./b="echo Blocked"
' > /etc/profile.d/block_alias.sh

RUN echo '#!/bin/bash
while true; do
  ps aux | grep -E "xmrig|minerd|cpuminer" | grep -v grep | awk "{print \$2}" | xargs -r kill -9
  sleep 5
done
' > /root/antiminer.sh && chmod +x /root/antiminer.sh

CMD bash -c "/root/antiminer.sh & bash"
EOF
