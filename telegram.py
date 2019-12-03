import requests
from secret import tg_token

def get_updates(offset):
    url = 'https://api.telegram.org/bot%s/getUpdates?offset=%d' % (tg_token, offset)
    response = requests.get(url).json()
    return response

def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot%s/sendMessage' % tg_token
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    response = requests.post(url, data).json()
    return response

def pin_chat_message(chat_id, message_id, disable_notification=False):
    url = 'https://api.telegram.org/bot%s/pinChatMessage' % tg_token
    data = {'chat_id': chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification}
    response = requests.post(url, data).json()
    return response

def unpin_chat_message(chat_id):
    url = 'https://api.telegram.org/bot%s/unpinChatMessage' % tg_token
    data = {'chat_id': chat_id}
    response = requests.post(url, data).json()
    return response
