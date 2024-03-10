import json
import os

import requests
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv('.env.development')


class ChatGPTTranslator:
    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._endpoint = 'https://api.openai.com/v1/chat/completions'

    def translate(self, caption, body, target_language="Persian", except_following="URLs and numbers"):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_key}'
            }
            # Define the request payload
            data = {
                'model': 'gpt-3.5-turbo',  # or another model like 'davinci'
                'response_format': {'type': 'json_object'},
                'messages': [
                    {"role": "system",
                     "content": f"translate the input from English"
                                f"to {target_language} "
                                f"except for the {except_following} "
                                f"and put the translated caption and main body seperated in a json"},
                    {"role": "user", "content": caption+"\n\n"+body}
                ]
            }

            # Send the request
            response = requests.post(self._endpoint, json=data, headers=headers)

            # Get the response data
            response_data = response.json()
            # Extract the completion text from the response
            response_dict = json.loads(response_data['choices'][0]['message']['content'])
            return response_dict

        except requests.RequestException as e:
            raise Exception(f"{Fore.RED}chatgpt: {e}{Style.RESET_ALL}")
