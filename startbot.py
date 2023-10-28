#!/usr/bin/env python

import time
import telepot
import syslog
from telepot.loop import MessageLoop
from telegram_bot import read_bot_token, handle_command

# Your script's version number
SCRIPT_VERSION = "0.31"
CHAT_ID_FILE = '/usr/local/bin/tgbot/chat_ids.txt'

# Load the whitelist
def load_whitelist():
    with open(CHAT_ID_FILE, 'r') as f:
        return {line.strip() for line in f}

whitelist = load_whitelist()

def send_message_to_all_users(message):
    if whitelist:  # Check if whitelist is not empty
        for chat_id in whitelist:
            bot.sendMessage(chat_id, message)
    else:
        syslog.syslog('No chat IDs in whitelist. Not sending the message.')


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    # Check if the chat_id is in whitelist or if the whitelist is empty
    if not whitelist or str(chat_id) in whitelist:
        syslog.syslog('Received command: %s' % command)
        response = handle_command(command, chat_id)
        bot.sendMessage(chat_id, response)
    else:
        syslog.syslog('Received command from non-whitelisted ID: %s' % chat_id)

bot_token = read_bot_token()
bot = telepot.Bot(bot_token)

# Broadcast bot service started
send_message_to_all_users('Bot service started (version %s)' % SCRIPT_VERSION)

MessageLoop(bot, handle).run_as_thread()
syslog.syslog('Bot service started (version %s)' % SCRIPT_VERSION)

while True:
    time.sleep(10)
