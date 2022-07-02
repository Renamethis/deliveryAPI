import requests

class TelegramBot:
    
    def __init__(self, token="5307752489:AAGh9q6-K2TtLTgvuZZ7QDFZipa_6obtcI0"):
        self.__token = token

    def send_text(self, text):
        response = requests.get("https://api.telegram.org/bot" + \
            self.__token + "/getUpdates").json()
        ids = []
        if(response and response['ok'] == True):
            for update in response['result']:
                chat_id = update['message']['chat']['id']
                if(chat_id not in ids):
                    ids.append(chat_id)
                    url = 'https://api.telegram.org/bot' + self.__token + \
                        '/sendMessage?chat_id=' + str(chat_id) + \
                        '&parse_mode=Markdown&text='
                    response = requests.get(url + text)
                