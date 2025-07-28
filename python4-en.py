#Code By SNIPA VN chúng mày nhớ ghi bản quyền của tao

import discord
from discord.ext import commands, tasks
import subprocess
import re
import os
import uuid

TOKEN = ''  # Nhập token bot của bạn tại đây

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

SERVER_LIMIT = 12
database_file = 'database.txt'


def add_to_database(user, container_name, ssh_command):
    with open(database_file, 'a') as f:
        f.write(f"{user}|{container_name}|{ssh_command}\n")


def remove_from_database(ssh_command):
    if not os.path.exists(database_file):
        return
    with open(database_file, 'r') as f:
        lines = f.readlines()
    with open(database_file, 'w') as f:
        for line in lines:
            if ssh_command not in line:
                f.write(line)


def get_user_servers(user):
    if not os.path.exists(database_file):
        return []
    servers = []
    with open(database_file, 'r') as f:
        for line in f:
            if line.startswith(user):
                servers.append(line.strip())
    return servers


def count_user_servers(user):
    return len(get_user_servers(user))


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    await bot.tree.sync()


@bot.tree.command(name="list", description="Hiển thị tất cả VPS bạn đang có")
async def list_servers(interaction: discord.Interaction):
    user = str(interaction.user)
    servers = get_user_servers(user)
    if servers:
        embed = discord.Embed(title="Danh sách VPS của bạn", color=0x00ff00)
        for server in servers:
            _, container_name, _ = server.split('|')
            embed.add_field(name=container_name, value="Loại: uDocker Container", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=discord.Embed(description="❌ Bạn chưa có VPS nào.", color=0xff0000))


@bot.tree.command(name="deploy-ubuntu", description="Tạo VPS Ubuntu 22.04")
async def deploy_ubuntu(interaction: discord.Interaction):
    user = str(interaction.user)

    if count_user_servers(user) >= SERVER_LIMIT:
        await interaction.response.send_message(embed=discord.Embed(description="❌ Đã vượt quá giới hạn VPS!", color=0xff0000))
        return

    await interaction.response.send_message(embed=discord.Embed(description="⏳ Đang tạo VPS Ubuntu 22.04...", color=0x00ff00))

    container_name = f"vps_{uuid.uuid4().hex[:8]}"
    image = "ubuntu:22.04"
    commands = "apt update && apt install -y tmate && tmate -F"

    # Tải image nếu chưa có
    subprocess.run(["udocker", "pull", image])

    # Tạo container
    subprocess.run(["udocker", "create", "--name", container_name, image])

    # Chạy container và thu thập output
    process = subprocess.Popen(
        ["udocker", "run", "--name", container_name, "sh", "-c", commands],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    ssh_link = None
    for line in iter(process.stdout.readline, b''):
        decoded = line.decode('utf-8')
        match = re.search(r'ssh session: (ssh [^\n]+)', decoded)
        if match:
            ssh_link = match.group(1)
            break

    if ssh_link:
        add_to_database(user, container_name, ssh_link)
        await interaction.user.send(embed=discord.Embed(
            description=f"### ✅ VPS đã tạo\nSSH: ```{ssh_link}```\nOS: Ubuntu 22.04\n🔗 [Discord Support](https://dsc.gg/servertipacvn)",
            color=0x00ff00
        ))
        await interaction.followup.send(embed=discord.Embed(description="✅ VPS đã được gửi vào DM của bạn.", color=0x00ff00))
    else:
        await interaction.followup.send(embed=discord.Embed(description="❌ VPS tạo thất bại hoặc quá lâu không phản hồi.", color=0xff0000))
        subprocess.run(["udocker", "rm", "-f", container_name])


@bot.tree.command(name="remove", description="Xoá VPS theo SSH command")
async def remove(interaction: discord.Interaction, ssh_command: str):
    user = str(interaction.user)
    servers = get_user_servers(user)
    matched = [s for s in servers if ssh_command in s]

    if not matched:
        await interaction.response.send_message(embed=discord.Embed(description="❌ Không tìm thấy VPS với SSH đó.", color=0xff0000))
        return

    container_name = matched[0].split('|')[1]
    subprocess.run(["udocker", "rm", "-f", container_name])
    remove_from_database(ssh_command)

    await interaction.response.send_message(embed=discord.Embed(description="✅ VPS đã xoá thành công.", color=0x00ff00))


bot.run(TOKEN)
