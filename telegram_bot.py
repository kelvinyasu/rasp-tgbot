# telegram_bot.py

import subprocess
import socket
import datetime
import telepot
import syslog
import os
import random

# Your script's version number
SCRIPT_VERSION = "0.31"

# File to store chat IDs
CHAT_ID_FILE = '/usr/local/bin/tgbot/chat_ids.txt'

# Variable to store the Git commit hash
GIT_COMMIT_HASH = None

# Restart Service Scripts
script_path = '/usr/local/bin/tgbot/restartservice.sh'


def read_bot_token():
    with open('/usr/local/bin/tgbot/bot.txt', 'r') as f:
        return f.read().strip()

def get_chat_id(message):
    # Extract the chat_id from the message dictionary
    chat_id = message['chat']['id']
    return chat_id

def log_chat_id(chat_id):
    # Read existing chat IDs from the file
    existing_chat_ids = set()
    try:
        with open(CHAT_ID_FILE, 'r') as f:
            existing_chat_ids = set(line.strip() for line in f)
    except FileNotFoundError:
        pass

    # Check if the chat ID is already in the set of existing IDs
    if str(chat_id) not in existing_chat_ids:
        # Append the chat ID to the chat IDs file
        with open(CHAT_ID_FILE, 'a') as f:
            f.write(str(chat_id) + '\n')

def handle_command(command, chat_id):
    log_chat_id(chat_id)  # Log the chat ID
    
    if command == '/roll':
        return random.randint(1, 6)
    elif command == '/time':
        return str(datetime.datetime.now())
    elif command == '/reboot':
        # Add a 2-second delay before rebooting
        subprocess.call(['sudo', 'pkill', 'openvpn'])
        subprocess.call(['sudo', 'shutdown', '-r', '+2'])
        return "Stop VPN & Rebooting..."
    elif command == '/network':
        return get_network_info()
    elif command == '/syslog':
        return get_last_syslog_lines(20)
    elif command == '/chatid':
        return f"Your chat ID is: {chat_id}"
    elif command == '/upgrade':
        return upgrade_bot()
    else:
        hostname = socket.gethostname()
        return read_bot_motd() + f"\nUnknown command on {hostname}. Use /chatid, /roll, /time, /reboot, /network, /syslog, or /upgrade."

def get_network_info():
    interfaces = subprocess.check_output(['ip', 'addr', 'show']).decode('utf-8')
    interface_info = ""
    lines = interfaces.strip().split('\n')
    for line in lines:
        if line.startswith(" "):
            parts = line.strip().split()
            if parts[0] == "inet":
                interface_info += f"Interface: {parts[-1]}\tIP: {parts[1]}\n"
    external_ip = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
    interface_info += f"External IP: {external_ip}\n"
    return f"Network Interfaces and IP Addresses:\n{interface_info}"

def get_last_syslog_lines(num_lines):
    syslog_lines = subprocess.check_output(['tail', '-n', str(num_lines), '/var/log/syslog']).decode('utf-8')
    return f"Last {num_lines} lines of syslog:\n{syslog_lines}"

def upgrade_bot():
    # Save a copy of the current bot.txt file
    current_bot_txt = None
    with open('/usr/local/bin/tgbot/bot.txt', 'r') as f:
        current_bot_txt = f.read()

    try:
        # Change to the bot's directory
        os.chdir('/usr/local/bin/tgbot')

        # Discard any local changes and reset to the HEAD of the remote repository
        # subprocess.call(['git', 'reset', '--hard', 'HEAD'])

        # Pull the latest changes from the GitHub repository
        subprocess.call(['git', 'pull'])

        # Get the Git commit hash of the latest commit
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        GIT_COMMIT_HASH = git_hash  # Store the hash in the variable

        # Restore the original bot.txt file
        with open('/usr/local/bin/tgbot/bot.txt', 'w') as f:
            f.write(current_bot_txt)

        # Make the script file executable
        subprocess.call(['chmod', '+x', script_path])

        # Schedule a delayed service restart with 'at' command
        subprocess.call(['at', 'now + 1 minute', '-f', script_path])

        return f"Bot scheduled upgrade from version {SCRIPT_VERSION} with upcoming GIT hash {GIT_COMMIT_HASH}."
    except Exception as e:
        return f"Bot upgrade failed: {str(e)}"

def read_bot_motd():
    motd_path = '/usr/local/bin/tgbot/botmotd.txt'
    try:
        with open(motd_path, 'r') as f:
            # Read the file, filter out lines starting with #, and join them into a single string
            content = ''.join(line for line in f if not line.strip().startswith('#'))
        return content.strip()  # Return the content, stripping any extra spaces or newlines
    except FileNotFoundError:
        return "MOTD file not found."
    except Exception as e:
        return f"Error reading MOTD: {str(e)}"

