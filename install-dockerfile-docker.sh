#!/bin/bash
clear
echo "SNIPA VN"
echo "YouTube : https://youtube.com/@snipavn205"
echo "------------------------"
echo "Wait 3s to install/Đợi 3s để cài"
sleep 3


while true; do
    echo "If there is no DNS, enter nodns or if there is DNS, enter dns/Không DNS thì nhập nodns hay có DNS thì nhập dns"
    echo "forced entry!!!!/bắt buộc phải nhập!!!!"
    read -rp ">> " meobell

    if [[ "$meobell" == "dns" || "$meobell" == "nodns" ]]; then
        break
    else
        echo "❌ Only 'dns' or 'nodns' can be entered. Please try again./❌ Chỉ được nhập 'dns' hoặc 'nodns'. Vui lòng thử lại."
    fi
done


bash <(curl -Ls "https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile-$meobell/install-dockerfile-debian.sh")
bash <(curl -Ls "https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile-$meobell/install-dockerfile-ubuntu.sh")
bash <(curl -Ls "https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile-$meobell/install-dockerfile-fedora.sh")
bash <(curl -Ls "https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/dockerfile-$meobell/install-dockerfile-alpine.sh")

echo " Made successfully - Building Docker image."
echo " Building Docker Image/Xây dựng hình ảnh Docker"
sudo docker build -t ubuntu-22.04-with-tmate -f Dockerfile1 .
sudo docker build -t debian-with-tmate -f Dockerfile2 .
sudo docker build -t alpine-with-tmate -f Dockerfile3 .
sudo docker build -t fedora-with-tmate -f Dockerfile4 .
echo " Built successfully/Xây dựng thành công"
