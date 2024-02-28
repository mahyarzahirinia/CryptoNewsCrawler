import os

import requests
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()


class ChatGPTTranslator:
    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._endpoint = 'https://api.openai.com/v1/completions'

    def translate(self, text, target_language="Persian", except_following="urls and numbers"):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_key}'
            }
            # Define the request payload
            data = {
                'model': 'gpt-3.5-turbo',  # or another model like 'davinci'
                'prompt': f"translate the text which is related to cryptocurrency news "
                          f"to {target_language} "
                          f"except for the {except_following} "
                          f"and maintain the formatted string intact please\n"
            }

            # Send the request
            response = requests.post(self._endpoint, json=data, headers=headers)

            # Get the response data
            response_data = response.json()
            # Extract the completion text from the response
            completion_text = response_data['choices'][0]['text'].strip()
            return completion_text

        except Exception as e:
            raise Exception(f"{Fore.RED}{e}{Style.RESET_ALL}")
