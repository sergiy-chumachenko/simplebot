import requests
import logging
from time import sleep

BOT_TOKEN = '<your_bot_token>'
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def get_last_updates():
    response = requests.get(url=URL + 'getUpdates')
    return response.json()


def last_update(data):
    if data.get('ok'):
        try:
            last_update = data['result'][-1]
        except (KeyError, IndexError) as e:
            logging.error("Unable to get last result from data. %s", e)
        else:
            return last_update
    else:
        logging.error('Something goes wrong!')
        raise requests.exceptions.RequestException


def get_chat_id(update):
    return update['message']['chat']['id']


def send_msg(chat_id, msg):
    params = {
        'chat_id': chat_id,
        'text': msg
    }
    response = requests.post(url=URL + 'sendMessage', data=params)
    return response


def main():
    try:
        update_id = last_update(get_last_updates()).get('update_id')
        while True:
            update = last_update(get_last_updates())
            last_upd_id = update.get('update_id')
            logging.info(f"Last update id: {last_upd_id}")
            if update_id == last_upd_id:
                send_msg(chat_id=get_chat_id(update), msg='test')
                update_id += 1
            sleep(1)
    except requests.exceptions.RequestException as e:
        logging.error('Request Error! %s', e)


if __name__ == "__main__":
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)
    logging.info('Start talking...')
    main()
