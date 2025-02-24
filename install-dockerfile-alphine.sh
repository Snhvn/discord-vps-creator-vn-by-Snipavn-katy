cat <<EOF > Dockerfile3
FROM alpine:3.14

RUN apt update
RUN apt install -y tmate
EOF
