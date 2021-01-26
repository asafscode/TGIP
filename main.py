#!/usr/bin/env python3
import sys
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

my_user = None


def send_ip(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id.real == my_user:
        print("Sending IP to authorized user...")
        try:
            resp = requests.get("https://ifconfig.me", timeout=10)
        except:
            update.message.reply_text("it ain't workin atm")
            return
        update.message.reply_text(resp.text)
    else:
        print(f"Unauthorized access attempt from user ID: {update.effective_user.id.real}")
        update.message.reply_text("gtfo")


def main():
    global my_user
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <bot_token> <autorized_user_id>")
        exit(1)
    bot_token = sys.argv[1]
    try:
        my_user = int(sys.argv[2])
    except ValueError:
        print("Give me a valid user ID, not this garbage...")
        exit(1)
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("send_ip", send_ip))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
