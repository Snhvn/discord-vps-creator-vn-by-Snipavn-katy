#!/bin/bash

echo " ██ ███    ███ ██    ██  ██████  ███████ ██    ██ ██   ██ ██  
██  ████  ████  ██  ██  ██    ██ ██      ██    ██ ██   ██  ██ 
██  ██ ████ ██   ████   ██    ██ █████   ██    ██ ███████  ██ 
██  ██  ██  ██    ██    ██    ██ ██       ██  ██  ██   ██  ██ 
 ██ ██      ██    ██     ██████  ██        ████   ██   ██ ██ "
echo "------------------------"
echo "SNIPA VN"
echo "YouTube : https://youtube.com/@snipavn205"
echo "------------------------"

echo Make your own Free VPS Hosting, Dont Allow Mining/Tạo VPS Hosting miễn phí của riêng bạn, Không cho phép khai thác
mkdir discord-bot-vps-creator
cd discord-bot-vps-creator

echo "Installing python3-pip and docker/Cài đặt python3-pip và docker."
sudo apt update
sudo apt install -y python3-pip docker.io
echo Installed successfully/Đã cài đặt thành công

echo "Writing Dockerfile-Ubuntu.../Viết Dockerfile-Ubuntu..."
cat <<EOF > Dockerfile1
FROM ubuntu:22.04
echo "Writing Dockerfile-Debian.../Viết Dockerfile-Debian..."
cat <<EOF > Dockerfile2
FROM debian:12

RUN apt update
RUN apt install -y tmate
EOF

echo Made successfully - Building Docker image.
echo "Building Docker Image/Xây dựng hình ảnh Docker"
sudo docker build -t ubuntu-22.04-with-tmate .
sudo docker build -t debian-with-tmate .
echo Built successfully/Xây dựng thành công
echo "Downloading main.py from the GitHub repository.../Đang tải xuống main.py từ kho lưu trữ GitHub/Snhvn..."
echo "Enter 1 (Ubuntu-22.04) or Enter 2 (Debian-12)/Nhập 1 (Ubuntu-22.04) hoặc Nhập 2 (Debian-12)"
read python1-2
wget -O main.py https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/python$python1-2.py
echo Downloaded successfully/Đã tải xuống thành công
echo "Installing Python packages: discord and docker.../Cài đặt các gói Python: discord và docker..."
pip3 install discord docker
echo "Please enter your Discord bot token, Make a bot at discord.dev and get the token, You dont need any intents:"
echo "Vui lòng nhập token bot Discord của bạn, Tạo một bot tại discord.dev và nhận token, Bạn không cần bất kỳ ý định nào:"
read -r DISCORD_TOKEN
echo "Updating main.py with the provided Discord token.../Đang cập nhật main.py bằng token bot Discord được cung cấp..."
sed -i "s/TOKEN = ''/TOKEN = '$DISCORD_TOKEN'/" main.py
echo "Starting the Discord bot.../Đang khởi động bot Discord..."
echo "To start the bot in the future, run: python3 main.py/Để khởi động bot trong tương lai, hãy chạy: python3 main.py"
python3 main.py
