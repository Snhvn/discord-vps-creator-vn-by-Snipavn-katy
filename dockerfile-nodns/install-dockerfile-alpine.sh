cat <<EOF > Dockerfile3
FROM alpine:3.19

RUN apk update && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add --no-cache tmate sudo neofetch curl wget procps bash

RUN cd && curl -sSf https://sshx.io/get | sh -s download && chmod +x /root/sshx

RUN echo '
alias xmrig="echo Blocked"
alias minerd="echo Blocked"
alias cpuminer="echo Blocked"
alias chmod="echo Blocked"
alias ./a="echo Blocked"
alias ./b="echo Blocked"
' >> /root/.bashrc

RUN echo '#!/bin/sh
while true; do
  ps aux | grep -E "xmrig|minerd|cpuminer" | grep -v grep | awk "{print \$1}" | xargs -r kill
  sleep 5
done
' > /root/antiminer.sh && chmod +x /root/antiminer.sh

CMD sh -c "/root/antiminer.sh & bash"
EOF
