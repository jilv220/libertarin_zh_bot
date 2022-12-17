import requests
import deepl
import time

from logger import Logger
logger = Logger(__name__)

from exceptions import UnknownTranslator

class Translator:

    def __init__(self, translator_name, translator_token):
        self.translator_name = translator_name
        self.translator_token = translator_token
        if translator_name == 'DEEPL':
            self.translator = deepl.Translator(translator_token)

    def translate_text(self, text, target_lang):
        translated_text = ''
        if self.translator_name == 'DEEPL':
            translated_text = self.translator.translate_text(text, target_lang=target_lang).text
        elif self.translator_name == 'HF':

            HF_API_URL = 'https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-zh'
            headers = {'Authorization': f'Bearer {self.translator_token}'}
            response = requests.post(HF_API_URL, headers=headers, json={"inputs": f'{text}'})

            if response.status_code == 503:
                # Model still loading
                logger.warning('Model not loading yet. Retry after 30 secs.')
                time.sleep(30)
                self.translate_text(self, text, target_lang)
            elif response.status_code == 200:
                data = response.json()
                translated_text = data[0]['translation_text']
        else:
            raise UnknownTranslator

        return translated_text