#!/usr/bin/env python

import time
import telepot
import syslog
from telepot.loop import MessageLoop
from telegram_bot import read_bot_token, handle_command

# File to store chat IDs
CHAT_ID_FILE = '/usr/local/bin/tgbot/chat_ids.txt'

# "Writing new function with telepot to send message to all user on chat_ids.txt"
def send_message_to_all_users(message):
    with open(CHAT_ID_FILE, 'r') as f:
        for line in f:
            chat_id = line.strip()
            bot.sendMessage(chat_id, message)

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    syslog.syslog('Received command: %s' % command)

    response = handle_command(command, chat_id)
    bot.sendMessage(chat_id, response)

bot_token = read_bot_token()
bot = telepot.Bot(bot_token)

# Broadbast bot service started
send_message_to_all_users('Bot service started')

MessageLoop(bot, handle).run_as_thread()
syslog.syslog('Bot service started')

while True:
    time.sleep(10)

