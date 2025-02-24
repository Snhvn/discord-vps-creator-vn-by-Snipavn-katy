import random # This is random bullshit
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

TOKEN = '' # TOKEN HERE
RAM_LIMIT = '2g'
SERVER_LIMIT = 2
database_file = 'database.txt'

intents = discord.Intents.default()
intents.messages = False
intents.message_content = False

bot = commands.Bot(command_prefix='/', intents=intents)
client = docker.from_env()

# port gen forward module < i forgot this shit in the start
def generate_random_port(): 
    return random.randint(1025, 65535)

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
                return line.split('|')[2]
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

def get_container_id_from_database(user):
    servers = get_user_servers(user)
    if servers:
        return servers[0].split('|')[1]
    return None

@bot.event
async def on_ready():
    change_status.start()
    print(f'Bot is ready. Logged in as {bot.user}')
    await bot.tree.sync()

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
        print(f"Failed to update status: {e}")

async def regen_ssh_command(interaction: discord.Interaction, container_name: str):
    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="No active instance found for your user.", color=0xff0000))
        return

    try:
        exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(embed=discord.Embed(description=f"Error executing tmate in Docker container: {e}", color=0xff0000))
        return

    ssh_session_line = await capture_ssh_session_line(exec_cmd)
    if ssh_session_line:
        await interaction.response.send_message(embed=discord.Embed(description="<:an_ba_to_com:1174718866732101735>Phiên SSH mới đã được tạo. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(description="<:hetcuunoi:1125772819381366824>Không thể tạo phiên SSH mới.", color=0xff0000))

async def start_server(interaction: discord.Interaction, container_name: str):
    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="<:AC_meow:1174719189429276682>Không tìm thấy Instance nào cho người dùng của bạn.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "start", container_id], check=True)
        exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        ssh_session_line = await capture_ssh_session_line(exec_cmd)
        if ssh_session_line:
            await interaction.user.send(embed=discord.Embed(description=f"<:AC_meow:1174719189429276682>Instance Bắt đầu\nLệnh phiên SSH: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)", color=0x00ff00))
            await interaction.response.send_message(embed=discord.Embed(description="Phiên bản đã khởi động thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(description="Instance started, but failed to get SSH session line.", color=0xff0000))
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(embed=discord.Embed(description=f"Error starting instance: {e}", color=0xff0000))

async def stop_server(interaction: discord.Interaction, container_name: str):
    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="No instance found for your user.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "stop", container_id], check=True)
        await interaction.response.send_message(embed=discord.Embed(description="Instance stopped successfully.", color=0x00ff00))
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(embed=discord.Embed(description=f"Error stopping instance: {e}", color=0xff0000))

async def restart_server(interaction: discord.Interaction, container_name: str):
    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="No instance found for your user.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "restart", container_id], check=True)
        exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        ssh_session_line = await capture_ssh_session_line(exec_cmd)
        if ssh_session_line:
            await interaction.user.send(embed=discord.Embed(description=f"### <:AC_meow:1174719189429276682>Instance Khởi Động Lại\nLệnh phiên SSH: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)\nOS: Ubuntu 22.04", color=0x00ff00))
            await interaction.response.send_message(embed=discord.Embed(description="Phiên bản đã khởi động lại thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(description="Đã khởi động lại phiên bản nhưng không nhận được dòng phiên SSH.", color=0xff0000))
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(embed=discord.Embed(description=f"Lỗi khi khởi động lại phiên bản: {e}", color=0xff0000))

def get_container_id_from_database(user, container_name):
    if not os.path.exists(database_file):
        return None
    with open(database_file, 'r') as f:
        for line in f:
            if line.startswith(user) and container_name in line:
                return line.split('|')[1]
    return None

async def execute_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

PUBLIC_IP = '138.68.79.95'

async def capture_output(process, keyword):
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output = output.decode('utf-8').strip()
        if keyword in output:
            return output
    return None

@bot.tree.command(name="port-add", description="Adds a port forwarding rule")
@app_commands.describe(container_name="The name of the container", container_port="The port in the container")
async def port_add(interaction: discord.Interaction, container_name: str, container_port: int):
    await interaction.response.send_message(embed=discord.Embed(description="Setting up port forwarding. This might take a moment...", color=0x00ff00))

    public_port = generate_random_port()

    # Set up port forwarding inside the container
    command = f"ssh -o StrictHostKeyChecking=no -R {public_port}:localhost:{container_port} serveo.net -N -f"

    try:
        # Run the command in the background using Docker exec
        await asyncio.create_subprocess_exec(
            "docker", "exec", container_name, "bash", "-c", command,
            stdout=asyncio.subprocess.DEVNULL,  # No need to capture output
            stderr=asyncio.subprocess.DEVNULL  # No need to capture errors
        )

        # Respond immediately with the port and public IP
        await interaction.followup.send(embed=discord.Embed(description=f"Port added successfully. Your service is hosted on {PUBLIC_IP}:{public_port}.", color=0x00ff00))

    except Exception as e:
        await interaction.followup.send(embed=discord.Embed(description=f"An unexpected error occurred: {e}", color=0xff0000))

@bot.tree.command(name="port-http", description="Forward HTTP traffic to your container")
@app_commands.describe(container_name="The name of your container", container_port="The port inside the container to forward")
async def port_forward_website(interaction: discord.Interaction, container_name: str, container_port: int):
    try:
        exec_cmd = await asyncio.create_subprocess_exec(
            "docker", "exec", container_name, "ssh", "-o StrictHostKeyChecking=no", "-R", f"80:localhost:{container_port}", "serveo.net",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        url_line = await capture_output(exec_cmd, "Forwarding HTTP traffic from")
        if url_line:
            url = url_line.split(" ")[-1]
            await interaction.response.send_message(embed=discord.Embed(description=f"Website forwarded successfully. Your website is accessible at {url}.", color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(description="Failed to capture forwarding URL.", color=0xff0000))
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(embed=discord.Embed(description=f"Error executing website forwarding: {e}", color=0xff0000))

async def create_server_task(interaction):
    await interaction.response.send_message(embed=discord.Embed(description="Creating Instance, This takes a few seconds.", color=0x00ff00))
    user = str(interaction.user)
    if count_user_servers(user) >= SERVER_LIMIT:
        await interaction.followup.send(embed=discord.Embed(description="```Error: Instance Limit-reached```", color=0xff0000))
        return

    image = "ubuntu-22.04-with-tmate"
    
    try:
        container_id = subprocess.check_output([
            "docker", "run", "-itd", "--privileged", "--cap-add=ALL", image
        ]).strip().decode('utf-8')
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(embed=discord.Embed(description=f"Error creating Docker container: {e}", color=0xff0000))
        return

    try:
        exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(embed=discord.Embed(description=f"Error executing tmate in Docker container: {e}", color=0xff0000))
        subprocess.run(["docker", "kill", container_id])
        subprocess.run(["docker", "rm", container_id])
        return

    ssh_session_line = await capture_ssh_session_line(exec_cmd)
    if ssh_session_line:
        await interaction.user.send(embed=discord.Embed(description=f"<:Himouto:1174718684590264413>Đã tạo thành công Instance\nSSH Session Command<:Himouto:1174718684590264413>: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)\nOS: Ubuntu 22.04", color=0x00ff00))
        add_to_database(user, container_id, ssh_session_line)
        await interaction.followup.send(embed=discord.Embed(description="VPS đã được tạo thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
    else:
        await interaction.followup.send(embed=discord.Embed(description="Something went wrong or the Instance is taking longer than expected. If this problem continues, Contact Support.", color=0xff0000))
        subprocess.run(["docker", "kill", container_id])
        subprocess.run(["docker", "rm", container_id])

async def create_server_task_debian(interaction):
    await interaction.response.send_message(embed=discord.Embed(description="Creating Instance, This takes a few seconds.", color=0x00ff00))
    user = str(interaction.user)
    if count_user_servers(user) >= SERVER_LIMIT:
        await interaction.followup.send(embed=discord.Embed(description="```Error: Instance Limit-reached```", color=0xff0000))
        return

    image = "debian-with-tmate"
    
    try:
        container_id = subprocess.check_output([
            "docker", "run", "-itd", "--privileged", "--cap-add=ALL", image
        ]).strip().decode('utf-8')
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(embed=discord.Embed(description=f"Error creating Docker container: {e}", color=0xff0000))
        return

    try:
        exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_id, "tmate", "-F",
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(embed=discord.Embed(description=f"Error executing tmate in Docker container: {e}", color=0xff0000))
        subprocess.run(["docker", "kill", container_id])
        subprocess.run(["docker", "rm", container_id])
        return

    ssh_session_line = await capture_ssh_session_line(exec_cmd)
    if ssh_session_line:
        await interaction.user.send(embed=discord.Embed(description=f"<:Himouto:1174718684590264413>Đã tạo thành công Instance\nSSH Session Command<:Himouto:1174718684590264413>: ```{ssh_session_line}```[Support Discord](https://dsc.gg/servertipacvn)\nOS: Debian 12", color=0x00ff00))
        add_to_database(user, container_id, ssh_session_line)
        await interaction.followup.send(embed=discord.Embed(description="Phiên bản đã được tạo thành công. Kiểm tra DM của bạn để biết chi tiết.", color=0x00ff00))
    else:
        await interaction.followup.send(embed=discord.Embed(description="Something went wrong or the Instance is taking longer than expected. If this problem continues, Contact Support.", color=0xff0000))
        subprocess.run(["docker", "kill", container_id])
        subprocess.run(["docker", "rm", container_id])

@bot.tree.command(name="deploy-ubuntu", description="Tạo một Instance mới với Ubuntu 22.04")
async def deploy_ubuntu(interaction: discord.Interaction):
    await create_server_task(interaction)

@bot.tree.command(name="deploy-debian", description="Tạo một Instance mới với Debian 12")
async def deploy_ubuntu(interaction: discord.Interaction):
    await create_server_task_debian(interaction)

@bot.tree.command(name="regen-ssh", description="Tạo một phiên SSH mới cho phiên bản của bạn")
@app_commands.describe(container_name="Tên/ssh-command của Instance của bạn")
async def regen_ssh(interaction: discord.Interaction, container_name: str):
    await regen_ssh_command(interaction, container_name)

@bot.tree.command(name="start", description="Bắt đầu Instances của bạn")
@app_commands.describe(container_name="Tên/ssh-command của Instance của bạn")
async def start(interaction: discord.Interaction, container_name: str):
    await start_server(interaction, container_name)

@bot.tree.command(name="stop", description="Dừng Instances của bạn")
@app_commands.describe(container_name="Tên/ssh-command của Instance của bạn")
async def stop(interaction: discord.Interaction, container_name: str):
    await stop_server(interaction, container_name)

@bot.tree.command(name="restart", description="Khởi động lại Instances của bạn")
@app_commands.describe(container_name="The name/ssh-command of your Instance")
async def restart(interaction: discord.Interaction, container_name: str):
    await restart_server(interaction, container_name)

@bot.tree.command(name="ping", description="Kiểm tra ping của bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="list", description="Liệt kê tất cả các Instances của bạn")
async def list_servers(interaction: discord.Interaction):
    user = str(interaction.user)
    servers = get_user_servers(user)
    if servers:
        embed = discord.Embed(title="Instances của bạn", color=0x00ff00)
        for server in servers:
            _, container_name, _ = server.split('|')
            embed.add_field(name=container_name, value="Mô tả: Một máy chủ với 16GB <:RAM:1147501868264722442>RAM và 4 <:cpu:1147496245766668338>Core.", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=discord.Embed(description="You have no servers.", color=0xff0000))

@bot.tree.command(name="remove", description="Xóa một Instances")
@app_commands.describe(container_name="Tên/ssh-command của Instances của bạn")
async def remove_server(interaction: discord.Interaction, container_name: str):
    user = str(interaction.user)
    container_id = get_container_id_from_database(user, container_name)

    if not container_id:
        await interaction.response.send_message(embed=discord.Embed(description="Không tìm thấy Instances nào cho người dùng của bạn có tên đó.", color=0xff0000))
        return

    try:
        subprocess.run(["docker", "stop", container_id], check=True)
        subprocess.run(["docker", "rm", container_id], check=True)
        
        remove_from_database(container_id)
        
        await interaction.response.send_message(embed=discord.Embed(description=f"Instance '{container_name}'đã xóa thành công.", color=0x00ff00))
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(embed=discord.Embed(description=f"Lỗi khi xóa instances: {e}", color=0xff0000))

@bot.tree.command(name="help", description="Hiển thị thông báo trợ giúp")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="<:info:1147509120149246062>Information<:info:1147509120149246062>", color=0x00ff00)
    embed.add_field(name="/deploy-ubuntu", value="Tạo một Instance mới với Ubuntu 22.04.", inline=False)
    embed.add_field(name="/deploy-debian", value="Tạo một Instance mới với Debian 12.", inline=False)
    embed.add_field(name="/remove <ssh_command/Name>", value="Xóa một máy chủ", inline=False)
    embed.add_field(name="/start <ssh_command/Name>", value="Khởi động máy chủ.", inline=False)
    embed.add_field(name="/stop <ssh_command/Name>", value="Dừng một máy chủ.", inline=False)
    embed.add_field(name="/regen-ssh <ssh_command/Name>", value="Tạo lại SSH credential", inline=False)
    embed.add_field(name="/restart <ssh_command/Name>", value="Dừng máy chủ.", inline=False)
    embed.add_field(name="/list", value="Liệt kê tất cả các máy chủ của bạn", inline=False)
    embed.add_field(name="/ping", value="Kiểm tra ping của bot.", inline=False)
    embed.add_field(name="/port-http", value="Chuyển tiếp một trang web http.", inline=False)
    embed.add_field(name="/port-add", value="Chuyển tiếp một cổng.", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
