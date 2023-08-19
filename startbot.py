#!/usr/bin/env python

import socket
import syslog
import time
import random
import datetime
import telepot
import subprocess
from telepot.loop import MessageLoop

def read_bot_token():
    with open('/usr/local/bin/tgbot/bot.txt', 'r') as f:
        return f.read().strip()

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    syslog.syslog('Received command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1, 6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/reboot':
        bot.sendMessage(chat_id, "Rebooting...")
        subprocess.call(['sudo', 'reboot'])
    elif command == '/network':
        network_info = get_network_info()
        bot.sendMessage(chat_id, network_info)
    elif command == '/syslog':
        syslog_output = get_last_syslog_lines(20)
        bot.sendMessage(chat_id, syslog_output)
    else:
        hostname = socket.gethostname()
        bot.sendMessage(chat_id, f"Unknown command on {hostname}. Use /roll, /time, /reboot, /network, or /syslog.")


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
    return "Last {} lines of syslog:\n{}".format(num_lines, syslog_lines)


bot_token = read_bot_token()
bot = telepot.Bot(bot_token)

MessageLoop(bot, handle).run_as_thread()
syslog.syslog('Bot service started')

while True:
    time.sleep(10)

