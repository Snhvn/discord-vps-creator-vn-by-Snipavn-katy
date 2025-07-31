cat <<EOF > Dockerfile3
FROM alpine:3.19

RUN echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
RUN apk update && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add --no-cache tmate && \
    apk add sudo neofetch curl wget
    
EOF
