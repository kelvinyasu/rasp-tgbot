# telegram_bot.py

import subprocess
import socket
import datetime
import telepot
import syslog
import os

def read_bot_token():
    with open('/usr/local/bin/tgbot/bot.txt', 'r') as f:
        return f.read().strip()

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
    elif command == '/upgrade':
        return upgrade_bot()
    else:
        hostname = socket.gethostname()
        return f"Unknown command on {hostname}.  Use /roll, /time, /reboot, /network, /syslog, or /upgrade."

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

        # Restore the original bot.txt file
        with open('/usr/local/bin/tgbot/bot.txt', 'w') as f:
            f.write(current_bot_txt)

        # Restart the service after upgrading
        subprocess.call(['systemctl', 'restart', 'telegram_bot'])

        return "Bot upgraded successfully."
    except Exception as e:
        return f"Bot upgrade failed: {str(e)}"
