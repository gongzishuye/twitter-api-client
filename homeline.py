import json
import re
import datetime
import traceback
import pytz

from twitter.account import Account
from collections import Counter
from apscheduler.schedulers.blocking import BlockingScheduler

from telegram_client import send_message


email, username, password = 'buptchenlu@gmail.com', 'moccachenlu', 'anloan00'
account = Account(email, username, password, debug=0, save=True)
utc = pytz.UTC


def string_to_datetime(string):
    """Converts a string to a datetime object.

    Args:
      string: The string to convert.

    Returns:
      A datetime object.
    """

    format_string = "%a %b %d %H:%M:%S %z %Y"
    try:
        return datetime.datetime.strptime(string, format_string)
    except ValueError:
        return None


def _satisfy_datetime(created_str, limit_datetime):
    if not limit_datetime:
        return True
    created_datetime = string_to_datetime(created_str)
    if not created_datetime:
        print('created datetime error None')
        return True
    if created_datetime.astimezone(pytz.UTC) >= limit_datetime.astimezone(pytz.UTC):
        return True
    return False


def get_homeline_interval():
    now = datetime.datetime.now()
    four_hour_ago = now - datetime.timedelta(hours=4)
    print(f'running schedule at {now}')
    latest_timeline = account.home_latest_timeline(limit=400)

    texts = []
    total_threads = 0
    for timeline in latest_timeline:
        entries = timeline['data']['home']['home_timeline_urt']['instructions'][0]['entries']
        total_threads += len(entries)

        for entry in entries:
            try:
                if 'items' in entry['content']:
                    result = entry['content']['items'][0]['item']['itemContent']['tweet_results']['result']
                else:
                    result = entry['content']['itemContent']['tweet_results']['result']
                rest_id = result['rest_id']
                name = result['core']['user_results']['result']['legacy']['screen_name']
                full_text = result['legacy']['full_text']
                create_at = result['legacy']['created_at']
                if result.get('quoted_status_result'):
                    quoted_status_result = result['quoted_status_result']
                    quoted_text = quoted_status_result['result']['legacy']['full_text']
                    full_text = f'{full_text}%%%%{quoted_text}'

                if _satisfy_datetime(create_at, four_hour_ago):
                    # print('do satisfy', name, rest_id, create_at)
                    texts.append(full_text)
                else:
                    # print('do not satisfy', name, rest_id, create_at)
                    pass
            except Exception as err:
                # print(f'Found error {err}')
                # print(json.dumps(entry))
                traceback.print_exc()

    print(f'total threads {total_threads}')
    return texts


def get_tokens(text):
    tokens_full = []
    pattern = r"\$([a-zA-Z0-9_.]+)"
    tokens = re.findall(pattern, text)
    tokens_full.extend(tokens)

    pattern = r"\#([a-zA-Z0-9_.]+)"
    tokens = re.findall(pattern, text)
    tokens_full.extend(tokens)

    return list(set(tokens_full))
    # return tokens_full


def get_token_counter(texts: list):
    words = []
    uni_words = set()
    for text in texts:
        tokens = get_tokens(text)
        tokens = [token.lower() for token in tokens if not (token.isnumeric() or token[0].isnumeric())]
        words.extend(tokens)
        uni_words.update(tokens)
        uni_words = set([word for word in uni_words if len(word) > 1])

    def contains_word(text, uni_words):
        words = set()
        for word in uni_words:
            if text.find(word) > -1:
                words.add(word)

        return list(words)

    total_words = []
    for text in texts:
        words = contains_word(text, uni_words)
        total_words.extend(words)
        counter = Counter(total_words)
    return counter


blacktokens = [
        'btc',
        'eth',
        'bitcoin',
        'ethereum',
        'altcoins',
        'altcoin',
        'crypto',
        'web3',
        'nfts',
        'tokens',
        'nft'
    ]
blacktokens = set(blacktokens)


def run():
    texts = get_homeline_interval()
    print(f'texts number: {len(texts)}')
    counter = get_token_counter(texts)
    print(counter.most_common())
    now = datetime.datetime.now()
    four_hour_ago = now - datetime.timedelta(hours=4)
    file_path = four_hour_ago.strftime("%Y-%m-%d-%H")
    with open(f'tw-tokens/{file_path}', 'w') as fw:
        for item in counter.most_common():
            if item[0] not in blacktokens and item[1] > 0:
                fw.write(f'{item[0]} {item[1]}\n')
                print(f'{item[0]} {item[1]}\n')

    with open(f'tw-tokens/{file_path}') as fr:
        content = fr.read()
    send_message(-853651755, f'{file_path}推特token rank：\n\n{content}')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'cron', hour='0,4,8,12,16,20,21', minute=39)

    scheduler.start()
