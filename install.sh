#!/bin/bash
INSTALL_FLAG="~/discord-bot-vps-creator/"
echo " ██ ███    ███ ██    ██  ██████  ███████ ██    ██ ██   ██ ██  
██  ████  ████  ██  ██  ██    ██ ██      ██    ██ ██   ██  ██ 
██  ██ ████ ██   ████   ██    ██ █████   ██    ██ ███████  ██ 
██  ██  ██  ██    ██    ██    ██ ██       ██  ██  ██   ██  ██ 
 ██ ██      ██    ██     ██████  ██        ████   ██   ██ ██ "
echo "------------------------"
echo "SNIPA VN"
echo "YouTube : https://youtube.com/@snipavn205"
echo "------------------------"
echo "Wait 3s to install/Đợi 3s để cài"
echo "Make your own Free VPS Hosting, Dont Allow Mining/Tạo VPS Hosting miễn phí của riêng bạn, Không cho phép khai thác"
if [ -f "$INSTALL_FLAG" ]; then
    read -p "\r\x1b[31;1m┃\x1b[0;31m Folder is already have had. Do you want to continue and will the folder be deleted?|Enter "y" to continue installation or enter "n" to exit...\x1b[0m" -n 1 -r 
fi
sleep 3
rm -rf discord-bot-vps-creator
mkdir -p discord-bot-vps-creator
cd discord-bot-vps-creator

echo "Installing python3-pip and docker/Cài đặt python3-pip và docker."
apt install -y sudo wget
sudo apt update
sudo apt install -y python3-pip
echo "Installing Docker (Ubuntu): Enter "docker" | Udocker (Ubuntu Clone): Enter "udocker"/Cài đặt Docker (Ubuntu): Nhập "docker" | Udocker (Bản sao Ubuntu): Nhập "udocker"."
read dockerorudocker
wget https://github.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/raw/refs/heads/main/install-$dockerorudocker.sh && chmod +x install-$dockerorudocker.sh && sudo ./install-$dockerorudocker.sh && rm install-$dockerorudocker.sh
echo Installed successfully/Đã cài đặt thành công
echo "Enter "docker": to install dockerfile | Enter "udocker": to install udockerfile"
read dockerfileorudockerfile
echo "Writing Dockerfile.../Viết Dockerfile..."
wget https://github.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/raw/refs/heads/main/install-dockerfile-$dockerfileorudockerfile.sh && chmod +x install-dockerfile-$dockerfileorudockerfile.sh && sudo ./install-dockerfile-$dockerfileorudockerfile.sh && rm install-dockerfile-$dockerfileorudockerfile.sh
echo "Downloading main.py from the GitHub repository.../Đang tải xuống main.py từ kho lưu trữ GitHub/Snhvn..."
echo -e "Enter "1-en" (English) (Ubuntu-22.04) or Enter "2-en" (English) (Full commands and add debian 12)/Nhập "1-vi" (Tiếng Việt) (Ubuntu-22.04) hoặc Nhập "2-vi" (Tiếng Việt) (Đầy đủ các lệnh và thêm debian-12), Nhập "3-vi" (Tiếng Việt) (Đầy đủ các lệnh và thêm Alpine và Fedora,..) "
read pythonnumber
wget -O main.py https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/python$pythonnumber.py
echo Downloaded successfully/Đã tải xuống thành công
echo "Installing Python packages: discord and docker.../Cài đặt các gói Python: discord và docker..."
pip3 install discord docker
clear
echo "Please enter your Discord bot token, Make a bot at discord.dev and get the token, You dont need any intents:"
echo "Vui lòng nhập token bot Discord của bạn, Tạo một bot tại discord.dev và nhận token, Bạn không cần bất kỳ ý định nào:"
read -r DISCORD_TOKEN
echo "Updating main.py with the provided Discord token.../Đang cập nhật main.py bằng token bot Discord được cung cấp..."
sed -i "s/TOKEN = ''/TOKEN = '$DISCORD_TOKEN'/" main.py
clear
echo "Starting the Discord bot.../Đang khởi động bot Discord..."
echo "To start the bot in the future, run: python3 main.py/Để khởi động bot trong tương lai, hãy chạy: python3 main.py"
python3 main.py
