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

echo Make your own Free VPS Hosting, Dont Allow Mining
mkdir discord-bot-vps-creator
cd discord-bot-vps-creator

echo "Installing python3-pip and docker."
sudo apt update
sudo apt install -y python3-pip docker.io
echo Installed successfully

echo "Writing Dockerfile..."
cat <<EOF > Dockerfile
FROM ubuntu:22.04

RUN apt update
RUN apt install -y tmate
EOF

echo Made successfully - Building Docker image.
echo "Building Docker Image"
sudo docker build -t ubuntu-22.04-with-tmate .
echo Built successfully
echo "Downloading main.py from the GitHub repository..."
wget -O main.py https://raw.githubusercontent.com/Snhvn/discord-vps-creator-vn-by-Snipavn-katy/refs/heads/main/python
echo Downloaded successfully
echo "Installing Python packages: discord and docker..."
pip3 install discord docker
echo "Please enter your Discord bot token, Make a bot at discord.dev and get the token, You dont need any intents:"
read -r DISCORD_TOKEN
echo "Updating main.py with the provided Discord token..."
sed -i "s/TOKEN = ''/TOKEN = '$DISCORD_TOKEN'/" main.py
echo "Starting the Discord bot..."
echo "To start the bot in the future, run: python3 main.py"
python3 main.py
