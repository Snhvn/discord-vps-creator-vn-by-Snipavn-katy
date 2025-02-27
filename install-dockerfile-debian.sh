cat <<EOF > Dockerfile1
FROM debian:12

RUN apt update
RUN apt install -y tmate

EOF
