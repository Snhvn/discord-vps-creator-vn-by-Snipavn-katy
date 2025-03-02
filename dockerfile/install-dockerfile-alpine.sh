cat <<EOF > Dockerfile3
FROM alpine:3.19

RUN apk update && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add --no-cache tmate && \
    apk add sudo neofetch curl wget
    
EOF
