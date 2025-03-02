cat <<EOF > Dockerfile5
FROM scratch

RUN opkg update -y && \
    opkg install -y tmate && \
    opkg install -y wget curl fastfetch sudo

EOF
