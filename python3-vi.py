import random
import logging
import subprocess
import sys
import os
import re
import time
import concurrent.futures
import discord
from discord.ext import commands, tasks
import docker
import asyncio
from discord import app_commands

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '' # TOKEN HERE
RAM_LIMIT = '2g'
SERVER_LIMIT = 1
database_file = 'database.txt'
# Add a list of allowed channel IDs
ALLOWED_CHANNEL_IDS = [1378918272812060742] # Replace with your actual channel IDs - Make sure it's a list!

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
client = docker.from_env()

# port gen forward module < i forgot this shit in the start
def generate_random_port():
    return random.randint(1025, 65535)

def add_to_database(user, container_name, ssh_command):
    with open(database_file, 'a') as f:
        f.write(f"{user}|{container_name}|{ssh_command}\n")

def remove_from_database(container_id):
    if not os.path.exists(database_file):
        return
    with open(database_file, 'r') as f:
        lines = f.readlines()
    with open(database_file, 'w') as f:
        for line in lines:
            if container_id not in line:
                f.write(line)

# Hàm để cập nhật lệnh SSH trong database
def update_ssh_command_in_database(user, container_id, new_ssh_command):
    if not os.path.exists(database_file):
        return
    updated_lines = []
    found = False
    with open(database_file, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 3 and parts[0] == user and parts[1] == container_id:
                updated_lines.append(f"{user}|{container_id}|{new_ssh_command}\n")
                found = True
            else:
                updated_lines.append(line)
    if found:
        with open(database_file, 'w') as f:
            f.writelines(updated_lines)
    else:
        # Nếu không tìm thấy, thêm mới (trường hợp này không nên xảy ra nếu container_id đã có)
        add_to_database(user, container_id, new_ssh_command)


async def capture_ssh_session_line(process):
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output = output.decode('utf-8').strip()
        if "ssh session:" in output:
            return output.split("ssh session:")[1].strip()
    return None

def get_ssh_command_from_database(container_id):
    if not os.path.exists(database_file):
        return None
    with open(database_file, 'r') as f:
        for line in f:
            if container_id in line:
                return line.split('|')[2].strip()
    return None

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

def get_container_id_from_database(user, container_identifier):
    """
    Tìm container ID từ tên container hoặc một phần của lệnh SSH.
    """
    if not os.path.exists(database_file):
        return None
    with open(database_file, 'r') as f:
        for line in f:
            parts = line.split('|')
            if len(parts) >= 3 and parts[0] == user:
                # Kiểm tra cả container_id (parts[1]) và lệnh SSH (parts[2])
                if container_identifier in parts[1] or container_identifier in parts[2]:
                    return parts[1] # Trả về container ID
    return None

@bot.event
async def on_ready():
    change_status.start()
    logger.info(f'Bot is ready. Logged in as {bot.user}')
    try:
        await bot.tree.sync()
        logger.info("Successfully synced application commands.")
    except Exception as e:
        logger.error(f"Failed to sync application commands: {e}")

@tasks.loop(seconds=5)
async def change_status():
    try:
        if os.path.exists(database_file):
            with open(database_file, 'r') as f:
                lines = f.readlines()
                instance_count = len(lines)
        else:
            instance_count = 0

        status = f"với {instance_count} Cloud Instances | dsc.gg/servertipacvn"
        await bot.change_presence(activity=discord.Game(name=status))
    except Exception as e:
        logger.error(f"Failed to update status: {e}")

def is_allowed_channel(interaction: discord.Interaction):
    return interaction.channel_id in ALLOWED_CHANNEL_IDS

async def regen_ssh_command_logic(interaction: discord.Interaction, container_identifier: str):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_identifier)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="Không tìm thấy phiên bản hoạt động nào cho người dùng của bạn.", color=0xff0000))
        return

    try:
        process = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    except Exception as e:
        logger.error(f"Error executing tmate in Docker container for regen-ssh: {e}")
        await interaction.response.send_message(embed=discord.Embed(description=f"Lỗi khi thực thi tmate trong container Docker: {e}", color=0xff0000))
        return

    ssh_session_line = await capture_ssh_session_line(process)
    if ssh_session_line:
        # Cập nhật lệnh SSH mới vào database
        update_ssh_command_in_database(user, container_id, ssh_session_line)
        await interaction.user.send(embed=discord.Embed(description=f"<:an_ba_to_com:1174718866732101735>Phiên SSH mới đã được tạo.\nLệnh phiên SSH: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)", color=0x00ff00))
        await interaction.response.send_message(embed=discord.Embed(description="<:an_ba_to_com:1174718866732101735>Phiên SSH mới đã được tạo. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(description="<:hetcuunoi:1125772819381366824>Không thể tạo phiên SSH mới. Vui lòng thử lại hoặc liên hệ hỗ trợ.", color=0xff0000))

async def start_server_logic(interaction: discord.Interaction, container_identifier: str):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_identifier)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="<:AC_meow:1174719189429276682>Không tìm thấy Instance nào cho người dùng của bạn.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "start", container_id], check=True, capture_output=True)
        process = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        ssh_session_line = await capture_ssh_session_line(process)
        if ssh_session_line:
            update_ssh_command_in_database(user, container_id, ssh_session_line)
            await interaction.user.send(embed=discord.Embed(description=f"<:AC_meow:1174719189429276682>Instance Bắt đầu\nLệnh phiên SSH: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)", color=0x00ff00))
            await interaction.response.send_message(embed=discord.Embed(description="Phiên bản đã khởi động thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(description="Instance started, but failed to get SSH session line.", color=0xff0000))
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting instance {container_id}: {e.stderr.decode()}")
        await interaction.response.send_message(embed=discord.Embed(description=f"Error starting instance: {e.stderr.decode()}", color=0xff0000))
    except Exception as e:
        logger.error(f"An unexpected error occurred during start_server: {e}")
        await interaction.response.send_message(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))

async def stop_server_logic(interaction: discord.Interaction, container_identifier: str):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_identifier)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="No instance found for your user.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "stop", container_id], check=True, capture_output=True)
        await interaction.response.send_message(embed=discord.Embed(description="Instance stopped successfully.", color=0x00ff00))
    except subprocess.CalledProcessError as e:
        logger.error(f"Error stopping instance {container_id}: {e.stderr.decode()}")
        await interaction.response.send_message(embed=discord.Embed(description=f"Error stopping instance: {e.stderr.decode()}", color=0xff0000))
    except Exception as e:
        logger.error(f"An unexpected error occurred during stop_server: {e}")
        await interaction.response.send_message(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))

async def restart_server_logic(interaction: discord.Interaction, container_identifier: str):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_identifier)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="No instance found for your user.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "restart", container_id], check=True, capture_output=True)
        process = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        ssh_session_line = await capture_ssh_session_line(process)
        if ssh_session_line:
            update_ssh_command_in_database(user, container_id, ssh_session_line)
            await interaction.user.send(embed=discord.Embed(description=f"### <:AC_meow:1174719189429276682>Instance Khởi Động Lại\nLệnh phiên SSH: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)\nOS: Ubuntu 22.04", color=0x00ff00))
            await interaction.response.send_message(embed=discord.Embed(description="Phiên bản đã khởi động lại thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(description="Đã khởi động lại phiên bản nhưng không nhận được dòng phiên SSH.", color=0xff0000))
    except subprocess.CalledProcessError as e:
        logger.error(f"Error restarting instance {container_id}: {e.stderr.decode()}")
        await interaction.response.send_message(embed=discord.Embed(description=f"Lỗi khi khởi động lại phiên bản: {e.stderr.decode()}", color=0xff0000))
    except Exception as e:
        logger.error(f"An unexpected error occurred during restart_server: {e}")
        await interaction.response.send_message(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))

PUBLIC_IP = '0.0.0.0' # Lưu ý: Đây không phải là IP công cộng thực sự của bạn. Bạn có thể cần một dịch vụ khác để lấy IP công cộng.

async def capture_output(process, keyword):
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output = output.decode('utf-8').strip()
        if keyword in output:
            return output
    return None

@bot.tree.command(name="port-add", description="Chuyển tiếp cổng cho Instance của bạn")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instance của bạn", container_port="Cổng trong Instance")
async def port_add(interaction: discord.Interaction, container_name: str, container_port: int):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    await interaction.response.send_message(embed=discord.Embed(description="Đang thiết lập chuyển tiếp cổng. Việc này có thể mất một lúc...", color=0x00ff00))

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.followup.send(embed=discord.Embed(description="Không tìm thấy Instance nào cho người dùng của bạn.", color=0xff0000))
        return

    public_port = generate_random_port()

    # Set up port forwarding inside the container using serveo.net
    command = f"ssh -o StrictHostKeyChecking=no -R {public_port}:localhost:{container_port} serveo.net -N -f"

    try:
        subprocess.run(["docker", "exec", "-d", container_id, "bash", "-c", command], check=True, capture_output=True)

        await interaction.followup.send(embed=discord.Embed(description=f"Cổng đã được thêm thành công. Dịch vụ của bạn có thể truy cập trên `{PUBLIC_IP}:{public_port}`. Vui lòng lưu ý: IP công cộng có thể thay đổi và dịch vụ này phụ thuộc vào serveo.net.", color=0x00ff00))

    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing port-add command in Docker container {container_id}: {e.stderr.decode()}")
        await interaction.followup.send(embed=discord.Embed(description=f"Lỗi khi thiết lập chuyển tiếp cổng: {e.stderr.decode()}", color=0xff0000))
    except Exception as e:
        logger.error(f"An unexpected error occurred during port_add: {e}")
        await interaction.followup.send(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))


@bot.tree.command(name="port-http", description="Chuyển tiếp lưu lượng HTTP đến Instance của bạn")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instance của bạn", container_ngroktoken="Nhập ngrok token của bạn (Tạo ngrok token: ngrok.com)", container_port="Cổng bên trong Instance để chuyển tiếp")
async def port_forward_website(interaction: discord.Interaction, container_name: str, container_ngroktoken: str, container_port: int):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    await interaction.response.send_message(embed=discord.Embed(description="Đang thiết lập chuyển tiếp HTTP. Việc này có thể mất một lúc...", color=0x00ff00))

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.followup.send(embed=discord.Embed(description="Không tìm thấy Instance nào cho người dùng của bạn.", color=0xff0000))
        return

    try:
        # Cài đặt và cấu hình ngrok trong container
        await execute_command(f"docker exec {container_id} apt update && apt install -y curl")
        await execute_command(f"docker exec {container_id} curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null")
        await execute_command(f"docker exec {container_id} echo \"deb https://ngrok-agent.s3.amazonaws.com/apt all main\" | tee /etc/apt/sources.list.d/ngrok.list")
        await execute_command(f"docker exec {container_id} apt update && apt install -y ngrok")

        # Cấu hình ngrok auth token
        await execute_command(f"docker exec {container_id} ngrok authtoken {container_ngroktoken}")

        # Chạy ngrok http tunnel ở chế độ nền
        subprocess.Popen(["docker", "exec", container_id, "ngrok", "http", str(container_port)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)

        await interaction.followup.send(embed=discord.Embed(description=f"Ngrok đã được khởi động trong container `{container_name}` cho cổng `{container_port}`. Vui lòng truy cập [ngrok dashboard](https://dashboard.ngrok.com/cloud-edge/tunnels) của bạn để lấy URL công khai.", color=0x00ff00))

    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing ngrok commands in Docker container {container_id}: {e.stderr.decode()}")
        await interaction.followup.send(embed=discord.Embed(description=f"Lỗi khi thiết lập chuyển tiếp HTTP với ngrok: {e.stderr.decode()}", color=0xff0000))
    except Exception as e:
        logger.error(f"An unexpected error occurred during port_forward_website: {e}")
        await interaction.followup.send(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))

async def execute_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command, stdout, stderr)
    return stdout.decode(), stderr.decode()


async def create_server_base_task(interaction: discord.Interaction, image: str, os_name: str, os_emoji: str):
    await interaction.response.send_message(embed=discord.Embed(description="Tạo Instance, mất vài giây.", color=0x00ff00))
    user = str(interaction.user)
    if count_user_servers(user) >= SERVER_LIMIT:
        await interaction.followup.send(embed=discord.Embed(description="```Đã hết lượt tạo vps```", color=0xff0000))
        return

    try:
        container_id = subprocess.check_output([
            "docker", "run", "-itd", "--hostname=servertipacvn", "--privileged", "--cap-add=ALL", image
        ]).strip().decode('utf-8')
        logger.info(f"Container {container_id} created successfully for user {user} with image {image}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating Docker container for {user} with image {image}: {e.stderr.decode()}")
        await interaction.followup.send(embed=discord.Embed(description=f"Lỗi khi tạo container Docker: {e.stderr.decode()}", color=0xff0000))
        return
    except Exception as e:
        logger.error(f"An unexpected error occurred during container creation: {e}")
        await interaction.followup.send(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))
        return

    try:
        process = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    except Exception as e:
        logger.error(f"Error executing tmate in Docker container {container_id}: {e}")
        await interaction.followup.send(embed=discord.Embed(description=f"Lỗi khi thực thi tmate trong container Docker: {e}", color=0xff0000))
        subprocess.run(["docker", "kill", container_id])
        subprocess.run(["docker", "rm", container_id])
        return

    ssh_session_line = await capture_ssh_session_line(process)
    if ssh_session_line:
        await interaction.user.send(embed=discord.Embed(description=f"<:Himouto:1174718684590264413>Đã tạo thành công Instance\nSSH Session Command<:Himouto:1174718684590264413>: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)\nOS:{os_emoji}{os_name}", color=0x00ff00))
        add_to_database(user, container_id, ssh_session_line) # Chỉ thêm vào database lần đầu
        await interaction.followup.send(embed=discord.Embed(description="VPS đã được tạo thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
    else:
        logger.warning(f"Failed to get SSH session line for container {container_id}.")
        await interaction.followup.send(embed=discord.Embed(description="Có gì đó không ổn hoặc Instance mất nhiều thời gian hơn dự kiến. Nếu sự cố này tiếp tục, Liên hệ Hỗ trợ.", color=0xff0000))
        subprocess.run(["docker", "kill", container_id])
        subprocess.run(["docker", "rm", container_id])

@bot.tree.command(name="deploy-ubuntu", description="Tạo một Instance mới với Ubuntu 22.04")
async def deploy_ubuntu(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong kênh <#1378918272812060742> vô sv t https://dsc.gg/servertipacvn.", color=0xff0000), ephemeral=True)
        return
    await create_server_base_task(interaction, "ubuntu-22.04-with-tmate", "Ubuntu 22.04", "<:ubuntu:1344300653324927046>")

@bot.tree.command(name="deploy-debian", description="Tạo một Instance mới với Debian 12")
async def deploy_debian(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong kênh <#1378918272812060742> vô sv t https://dsc.gg/servertipacvn.", color=0xff0000), ephemeral=True)
        return
    await create_server_base_task(interaction, "debian-with-tmate", "Debian 12", "<:debian:1344300752411164682>")

@bot.tree.command(name="deploy-alpine", description="Tạo một Instance mới với Alpine 3.19")
async def deploy_alpine(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong kênh <#1378918272812060742> vô sv t https://dsc.gg/servertipacvn.", color=0xff0000), ephemeral=True)
        return
    await create_server_base_task(interaction, "alpine-with-tmate", "Alpine 3.19", "<:alpine:1345340462055166012>")

@bot.tree.command(name="deploy-fedora", description="Tạo một Instance mới với Fedora")
async def deploy_fedora(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong kênh <#1378918272812060742> vô sv t https://dsc.gg/servertipacvn.", color=0xff0000), ephemeral=True)
        return
    await create_server_base_task(interaction, "fedora-with-tmate", "Fedora", "<:fedora:1345663440206827581>")

@bot.tree.command(name="regen-ssh", description="Tạo lại SSH credential cho Instance của bạn")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instance của bạn")
async def regen_ssh(interaction: discord.Interaction, container_name: str):
    await regen_ssh_command_logic(interaction, container_name)

@bot.tree.command(name="start", description="Khởi động Instance của bạn")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instance của bạn")
async def start(interaction: discord.Interaction, container_name: str):
    await start_server_logic(interaction, container_name)

@bot.tree.command(name="stop", description="Dừng Instance của bạn")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instance của bạn")
async def stop(interaction: discord.Interaction, container_name: str):
    await stop_server_logic(interaction, container_name)

@bot.tree.command(name="restart", description="Khởi động lại Instance của bạn")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instance của bạn")
async def restart(interaction: discord.Interaction, container_name: str):
    await restart_server_logic(interaction, container_name)

@bot.tree.command(name="ping", description="Kiểm tra ping của bot.")
async def ping(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🔴 Ping của bot!",
        description=f"Ping: {latency}ms",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="list", description="Liệt kê tất cả các Instances của bạn")
async def list_servers(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    user = str(interaction.user)
    servers = get_user_servers(user)
    if servers:
        embed = discord.Embed(title="Instances của bạn", color=0x00ff00)
        for server in servers:
            parts = server.split('|')
            if len(parts) >= 3:
                container_id_short = parts[1][:12] # Lấy 12 ký tự đầu của ID container
                # Không hiển thị ssh_command_full nữa
                embed.add_field(name=f"ID: `{container_id_short}`", value=f"Cấu hình: Một máy chủ với 16GB <:RAM:1147501868264722442>RAM và 4 <:cpu:1147496245766668338>Cpu.", inline=False)
            else:
                embed.add_field(name="Lỗi định dạng", value=f"Dữ liệu không hợp lệ: {server}", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=discord.Embed(description="Bạn không có máy chủ nào.", color=0xff0000))

@bot.tree.command(name="remove", description="Xóa một Instances")
@app_commands.describe(container_name="Tên/ID hoặc SSH Command của Instances của bạn")
async def remove_server(interaction: discord.Interaction, container_name: str):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="Không tìm thấy Instances nào cho người dùng của bạn có tên/ID đó.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "stop", container_id], check=True, capture_output=True)
        subprocess.run(["docker", "rm", container_id], check=True, capture_output=True)

        remove_from_database(container_id)

        await interaction.response.send_message(embed=discord.Embed(description=f"Instance `{container_id[:12]}` đã xóa thành công.", color=0x00ff00))
    except subprocess.CalledProcessError as e:
        logger.error(f"Error removing instance {container_id}: {e.stderr.decode()}")
        await interaction.response.send_message(embed=discord.Embed(description=f"Lỗi khi xóa instances: {e.stderr.decode()}", color=0xff0000))
    except Exception as e:
        logger.error(f"An unexpected error occurred during remove_server: {e}")
        await interaction.response.send_message(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))

@bot.tree.command(name="help", description="Hiển thị thông báo trợ giúp")
async def help_command(interaction: discord.Interaction):
    if not is_allowed_channel(interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Lệnh này chỉ có thể được sử dụng trong các kênh được phép.", color=0xff0000), ephemeral=True)
        return

    embed = discord.Embed(title="<:info:1147509120149246062>Information<:info:1147509120149246062>", color=0x00ff00)
    embed.add_field(name="<:ubuntu:1344300653324927046>|/deploy-ubuntu", value="Tạo một Instance mới với Ubuntu 22.04. Lệnh SSH sẽ được gửi vào DM của bạn.", inline=False)
    embed.add_field(name="<:debian:1344300752411164682>|/deploy-debian", value="Tạo một Instance mới với Debian 12. Lệnh SSH sẽ được gửi vào DM của bạn.", inline=False)
    embed.add_field(name="<:alpine:1345340462055166012>|/deploy-alpine", value="Tạo một Instance mới với Alpine 3.19. Lệnh SSH sẽ được gửi vào DM của bạn.", inline=False)
    embed.add_field(name="<:fedora:1345663440206827581>|/deploy-fedora", value="Tạo một Instance mới với Fedora. Lệnh SSH sẽ được gửi vào DM của bạn.", inline=False)
    embed.add_field(name="/remove <ssh_command/ID>", value="Xóa một máy chủ của bạn.", inline=False)
    embed.add_field(name="/start <ssh_command/ID>", value="Khởi động máy chủ của bạn.", inline=False)
    embed.add_field(name="/stop <ssh_command/ID>", value="Dừng một máy chủ của bạn.", inline=False)
    embed.add_field(name="/regen-ssh <ssh_command/ID>", value="Tạo lại SSH credential.", inline=False)
    embed.add_field(name="/restart <ssh_command/ID>", value="Khởi động lại máy chủ của bạn.", inline=False)
    embed.add_field(name="/list", value="Liệt kê tất cả các máy chủ của bạn.", inline=False)
    embed.add_field(name="/ping", value="Kiểm tra ping của bot.", inline=False)
    embed.add_field(name="/port-http <ssh_command/ID> <token ngrok> <cổng container>", value="Chuyển tiếp một trang web HTTP sử dụng ngrok.", inline=False)
    embed.add_field(name="/port-add <ssh_command/ID> <cổng container>", value="Chuyển tiếp một cổng sử dụng serveo.net.", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
