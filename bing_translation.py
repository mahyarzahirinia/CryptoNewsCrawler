import requests
import uuid


class BingTranslator:
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.base_url = 'https://api.cognitive.microsofttranslator.com'
        self.path = '/translate?api-version=3.0'

    def translate_text(self, text, to_language):
        params = f'&to={to_language}'

        constructed_url = self.base_url + self.path + params
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{'text': text}]
        response = requests.post(constructed_url, headers=headers, json=body)
        translated_text = response.json()[0]['translations'][0]['text']
        return translated_text

# Example usage:
translator = BingTranslator(subscription_key='your_subscription_key')
text_to_translate = 'Hello, how are you?'
translated_text = translator.translate_text(text_to_translate, 'fr')  # Translate to French
print(translated_text)
