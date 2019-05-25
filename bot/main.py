import requests
import logging
import os
import datetime


class BotHandler(object):
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(url=self.api_url + method, params=params)
        return response.json()

    def send_msg(self, chat_id, msg):
        method = 'sendMessage'
        params = {
            'chat_id': chat_id,
            'text': msg
        }
        response = requests.post(url=self.api_url + method, data=params)
        return response

    def get_last_update(self):
        get_result = self.get_updates()
        if get_result.get('ok'):
            result = get_result.get('result')
            if len(result) > 0:
                return result[-1]
            return
        else:
            raise requests.RequestException


simple_bot = BotHandler(token=os.environ.get('TELEGRAM_BOT_TOKEN'))
greetings = ("hi", "hello", "hi!", "hello!", "what's up?")
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        try:
            simple_bot.get_updates(new_offset)

            last_update = simple_bot.get_last_update()
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
        except (ValueError, requests.RequestException) as e:
            logging.error("An error has been occurred! %s", e)
        except TypeError:
            logging.info("Updates has not been found for now!")
        else:
            if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                simple_bot.send_msg(last_chat_id, 'Good morning, {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                simple_bot.send_msg(last_chat_id, 'Good afternoon, {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                simple_bot.send_msg(last_chat_id, 'Good evening, {}'.format(last_chat_name))
                # today += 1

            new_offset = last_update_id + 1


if __name__ == "__main__":
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)
    logging.info('Start talking...')
    try:
        main()
    except KeyboardInterrupt:
        exit()
