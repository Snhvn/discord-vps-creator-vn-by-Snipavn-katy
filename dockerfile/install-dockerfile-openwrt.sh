cat <<EOF > Dockerfile5
FROM scratch

RUN opkg update && \
    opkg install tmate && \
    opkg install wget && \
    opkg install curl && \
    opkg install fastfetch 

EOF
