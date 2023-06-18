"""
pip install python-telegram-bot --upgrade
"""
import datetime
import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # etc: /keyword show
    text = update.message.text
    # etc: show
    token = text[9:]
    files = os.listdir('twitter/tw-tokens')
    if not files:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Have not scrape any twitter.")
        return

    files.sort(reverse=True)
    files = files[:10]
    resp = ''
    for file in files:
        # dt = datetime.datetime.strptime(file, '%Y-%m-%d-%H')
        with open(f'twitter/tw-tokens/{file}') as f:
            lines = f.readlines()
            lines = [line for line in lines if line.split(' ')[0] == token]
            if lines:
                token_desc = lines[0]
                token_desc = token_desc.strip().split(' ')
                resp += f'{token_desc[0]} {token_desc[1]} {file}\n'
    if not resp:
        resp = f"Don't have this token {token}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)


async def rank():
    pass


if __name__ == '__main__':
    application = ApplicationBuilder().token('6083326207:AAHH-wfsGoaj1g1IU85T-ABAfuL71TkWIe8').build()

    start_handler = CommandHandler('keyword', keyword)
    application.add_handler(start_handler)
    start_handler = CommandHandler('rank', rank)
    application.add_handler(start_handler)

    application.run_polling()
