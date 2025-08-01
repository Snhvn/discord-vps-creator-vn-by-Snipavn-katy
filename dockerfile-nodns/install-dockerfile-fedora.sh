cat <<EOF > Dockerfile4
FROM fedora

RUN dnf update -y && \
    dnf install -y tmate wget fastfetch curl git systemctl sudo procps-ng bash

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN echo '
alias xmrig="echo Blocked"
alias minerd="echo Blocked"
alias cpuminer="echo Blocked"
alias chmod="echo Blocked"
alias ./a="echo Blocked"
alias ./b="echo Blocked"
' >> /root/.bashrc

RUN echo '#!/bin/bash
while true; do
  ps aux | grep -E "xmrig|minerd|cpuminer" | grep -v grep | awk "{print \$2}" | xargs -r kill -9
  sleep 5
done
' > /root/antiminer.sh && chmod +x /root/antiminer.sh

CMD bash -c "/root/antiminer.sh & bash"
EOF
