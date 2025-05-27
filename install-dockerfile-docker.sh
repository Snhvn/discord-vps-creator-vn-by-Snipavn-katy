#!/bin/bash
clear
echo "SNIPA VN"
echo "YouTube : https://youtube.com/@snipavn205"
echo "------------------------"
echo "Wait 3s to install/Đợi 3s để cài"
sleep 3

echo "Writing Dockerfile-Ubuntu.../Viết Dockerfile-Ubuntu"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-ubuntu.sh && chmod +x install-dockerfile-ubuntu.sh && sudo ./install-dockerfile-ubuntu.sh && rm install-dockerfile-ubuntu.sh
echo "Writing Dockerfile-Debian.../Viết Dockerfile-Debian"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-debian.sh && chmod +x install-dockerfile-debian.sh && sudo ./install-dockerfile-debian.sh && rm install-dockerfile-debian.sh
echo "Writing Dockerfile-Alpine.../Viết Dockerfile-Alpine"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-alpine.sh && chmod +x install-dockerfile-alpine.sh && sudo ./install-dockerfile-alpine.sh && rm install-dockerfile-alpine.sh
echo "Writing Dockerfile-Fedora.../Viết Dockerfile-Fedora"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-fedora.sh && chmod +x install-dockerfile-fedora.sh && sudo ./install-dockerfile-fedora.sh && install-dockerfile-fedora.sh
echo "Writing Dockerfile-Windows2012r2.../Viết Dockerfile-Windows2012r2"
wget https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile/install-dockerfile-windows2012r2.sh && chmod +x install-dockerfile-windows2012r2.sh && sudo ./install-dockerfile-windows2012r2.sh
echo Made successfully - Building Docker image.
echo "Building Docker Image/Xây dựng hình ảnh Docker"
sudo docker build -t ubuntu-22.04-with-tmate -f Dockerfile1 . && sudo docker build -t debian-with-tmate -f Dockerfile2 . && sudo docker build -t alpine-with-tmate -f Dockerfile3 . && sudo docker build -t fedora-with-tmate -f Dockerfile4 . && sudo docker build -t windows2012r2-with-sshx -f Dockerfile5 .
echo Built successfully/Xây dựng thành công
