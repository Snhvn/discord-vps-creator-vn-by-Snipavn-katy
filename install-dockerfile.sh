#!/bin/bash
clear
echo "SNIPA VN"
echo "YouTube : https://youtube.com/@snipavn205"
echo "------------------------"
echo "Wait 3s to install/Đợi 3s để cài"
sleep 3

echo "Writing Dockerfile-Ubuntu.../Viết Dockerfile-Ubuntu"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-ubuntu.sh && chmod +x install-dockerfile-ubuntu.sh && sudo ./install-dockerfile-ubuntu.sh
echo "Writing Dockerfile-Debian.../Viết Dockerfile-Debian"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-debian.sh && chmod +x install-dockerfile-debian.sh && sudo ./install-dockerfile-debian.sh
echo "Writing Dockerfile-Alpine.../Viết Dockerfile-Alpine"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-alpine.sh && chmod +x install-dockerfile-alpine.sh && sudo ./install-dockerfile-alpine.sh
echo "Writing Dockerfile-Fedora.../Viết Dockerfile-Fedora"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-fedora.sh && chmod +x install-dockerfile-fedora.sh && sudo ./install-dockerfile-fedora.sh
echo "Writing Dockerfile-Openwrt.../Viết Dockerfile-Openwrt"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-openwrt.sh && chmod +x install-dockerfile-openwrt.sh && sudo ./install-dockerfile-openwrt.sh
