#!/usr/bin/env python

import time
import telepot
import syslog
from telepot.loop import MessageLoop
from telegram_bot import read_bot_token, handle_command

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    syslog.syslog('Received command: %s' % command)

    response = handle_command(command, chat_id)
    bot.sendMessage(chat_id, response)

bot_token = read_bot_token()
bot = telepot.Bot(bot_token)

MessageLoop(bot, handle).run_as_thread()
syslog.syslog('Bot service started')

while True:
    time.sleep(10)
