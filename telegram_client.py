import asyncio

from telethon.sync import TelegramClient, events

# from scraper_utils import analysis_musk, analysis_news, analysis_job

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = '18135727'
api_hash = '2ba8c150264f728abff97adf2d2fde5e'


def send_message(chat, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TelegramClient('tele', api_id, api_hash, loop=loop) as client:
        client.send_message(chat, message)


# file_path = '2023-06-18-12'
# with open(f'twitter/tw-tokens/{file_path}') as fr:
#     content = fr.read()
# send_message(-853651755, f'{file_path}推特token rank：\n\n{content}')