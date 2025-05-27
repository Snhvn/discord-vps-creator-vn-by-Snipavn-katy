cat <<EOF > Dockerfile5
FROM debian:12

RUN apt update
RUN apt install qemu-utils qemu-system-x86 -y
RUN apt install -y curl wget sudo systemctl neofetch
RUN qemu-img create -f raw 2012r2.img
RUN wget https://github.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/raw/refs/heads/main/dockerfile/startwin.sh && sh startwin.sh
RUN curl -sSf https://sshx.io/get | sh -s run

EOF
