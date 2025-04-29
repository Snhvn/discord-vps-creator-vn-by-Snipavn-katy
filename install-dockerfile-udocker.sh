#!/bin/bash
clear
echo "SNIPA VN"
echo "YouTube : https://youtube.com/@snipavn205"
echo "------------------------"
echo "Wait 3s to install/Đợi 3s để cài"
sleep 3
echo "Writing UDockerfile-Ubuntu.../Viết Dockerfile-Ubuntu"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-ubuntu.sh && chmod +x install-dockerfile-ubuntu.sh && sudo ./install-dockerfile-ubuntu.sh && rm install-dockerfile-ubuntu.sh
echo "Writing UDockerfile-Debian.../Viết Dockerfile-Debian"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-debian.sh && chmod +x install-dockerfile-debian.sh && sudo ./install-dockerfile-debian.sh && rm install-dockerfile-debian.sh
echo "Writing UDockerfile-Alpine.../Viết Dockerfile-Alpine"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-alpine.sh && chmod +x install-dockerfile-alpine.sh && sudo ./install-dockerfile-alpine.sh && rm install-dockerfile-alpine.sh
echo "Writing UDockerfile-Fedora.../Viết Dockerfile-Fedora"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-fedora.sh && chmod +x install-dockerfile-fedora.sh && sudo ./install-dockerfile-fedora.sh && install-dockerfile-fedora.sh
echo "Writing UDockerfile-Openwrt.../Viết Dockerfile-Openwrt"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-openwrt.sh && chmod +x install-dockerfile-openwrt.sh && sudo ./install-dockerfile-openwrt.sh
echo Made successfully - Building UDocker image.
echo "Building UDocker Image/Xây dựng hình ảnh UDocker"
sudo -u discordvps udocker setup ubuntu-22.04-with-tmate -f Dockerfile1 . && sudo -u discordvps udocker setup -t debian-with-tmate -f Dockerfile2 . && sudo -u discordvps udocker setup -t alpine-with-tmate -f Dockerfile3 . && sudo -u discordvps udocker setup -t fedora-with-tmate -f Dockerfile4 . #&& sudo -u $newuser udocker setup -t openwrt-with-tmate -f Dockerfile5 .
echo Built successfully/Xây dựng thành công
