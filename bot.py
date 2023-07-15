import requests
import yaml
from db import cursor
from random import randint


def send_message(chat_id: int, text: str):
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(f'{BOT_API_URL}{BOT_API}/sendMessage', data=payload)


def get_latest_update_id(r):
    updates = r.json().get('result')
    if updates:
        latest_update = updates[-1]
        update_id = latest_update.get('update_id')
        return update_id


def get_message(r):
    message = r.json().get('result')[0].get('message')

    return message


def get_chat(r):
    chat = get_message(r).get('chat')

    return chat


def get_chat_id(r):
    id = get_chat(r).get('id')

    return id


def handle_commands(r):
    message = get_message(r)
    chat_id = get_chat_id(r)
    if message.get('text') == '/start':
        send_message(chat_id,  'Hi, I\'m hadith bot!')

    if message.get('text') == '/random':
        random_id = randint(1, 7277)
        cursor.execute('SELECT * FROM hadith WHERE id = ?', (random_id,))
        row = cursor.fetchone()

        if row:
            hadith_number = row[0]
            narrator = row[1]
            text_details = row[2]

            text = f'Hadith {hadith_number}/7277\n{narrator}\n{text_details}'
            send_message(chat_id, text)


def get_message_type(r):
    message_type = get_message(r).get('entities')[0].get('type')

    return message_type


with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    BOT_API = cfg.get('bot_api')
    BOT_API_URL = cfg.get('bot_api_url')
    update_id = None

    while True:
        r = requests.get(f'{BOT_API_URL}{BOT_API}/getUpdates', params={'offset': update_id})
        if r.status_code == 200:
            updates = r.json().get('result')
            if updates:
                update_id = get_latest_update_id(r) + 1
                for update in updates:
                    if 'message' in update and 'text' in update.get('message'):
                        handle_commands(r)

