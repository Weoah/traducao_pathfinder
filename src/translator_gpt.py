import openai
from time import sleep

from src.config import API_KEY, SYSTEM_ROLE, USER_ROLE
from src.dba import dba


class TranslatorGPT:

    def __init__(self) -> None:
        self.translated_data: dict = {}
        openai.api_key = API_KEY

    def translate_item(self, key, value, max_attemps=10, retry_delay=5):
        attemps = 0
        while attemps < max_attemps:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': SYSTEM_ROLE},
                    {'role': 'user', 'content': USER_ROLE + str(value)}
                ],
                temperature=0.2
            )

            translation = response.choices[0].message.content.strip()

            self.translated_data.update({'Key': key, 'Value': translation})
            self._insert_translated_data()
            print('\nTraduzindo a frase:', value)
            print('\nResultado:', translation)
            return translation

    def translate_one_item(self, item: dict):
        if dba.check_if_translated(item['Key']):
            return None
        self.translate_item(item['Key'], item['Value'])
        sleep(21)

    def _insert_translated_data(self) -> None:
        dba.insert_translated_data(self.translated_data)
        self.translated_data.clear()


translator = TranslatorGPT()
