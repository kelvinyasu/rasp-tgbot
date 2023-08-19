# telegram_bot.py

import subprocess
import socket
import datetime
import telepot
import syslog
import os

# Your script's version number
SCRIPT_VERSION = "1.0.0"

# Variable to store the Git commit hash
GIT_COMMIT_HASH = None

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
    if command == '/roll':
        return random.randint(1, 6)
    elif command == '/time':
        return str(datetime.datetime.now())
    elif command == '/reboot':
        subprocess.call(['sudo', 'reboot'])
        return "Rebooting..."
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
        return f"Hello, Unknown command on {hostname}. Use /chatid, /roll, /time, /reboot, /network, /syslog, or /upgrade."

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
        subprocess.call(['git', 'reset', '--hard', 'HEAD'])

        # Pull the latest changes from the GitHub repository
        subprocess.call(['git', 'pull'])

        # Get the Git commit hash of the latest commit
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        GIT_COMMIT_HASH = git_hash  # Store the hash in the variable

        # Restore the original bot.txt file
        with open('/usr/local/bin/tgbot/bot.txt', 'w') as f:
            f.write(current_bot_txt)

        # Schedule a delayed service restart with 'at' command
        subprocess.call(['echo', 'systemctl restart telegram_bot.service | at now + 1 minutes'], shell=True)

        return f"Bot upgraded successfully to version {SCRIPT_VERSION} with hash {GIT_COMMIT_HASH}."
    except Exception as e:
        return f"Bot upgrade failed: {str(e)}"
