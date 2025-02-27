cat <<EOF > Dockerfile2
FROM debian:12

RUN apt update
RUN apt install -y tmate

EOF
