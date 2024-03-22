import json
import os

import requests
from colorama import Fore, Style


class ChatGPTTranslator:
    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._endpoint = 'https://api.openai.com/v1/chat/completions'

    def translate(self, caption, body, target_language="Persian", except_following="URLs and numbers"):
        try:
            response_dict = None

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_key}'
            }
            # Define the request payload
            data = {
                'model': 'gpt-3.5-turbo-0125',
                'response_format': {'type': 'json_object'},
                'temperature': 0.45,
                'messages': [
                    {"role": "system",
                     "content": f"translate the input text from English"
                                f"to {target_language} "
                                f"except for the {except_following} "
                                f"and return the translated caption and "
                                f"main_body separated in a json"},
                    {"role": "user", "content": caption + "\n\n" + body}
                ]
            }

            # Send the request
            response = requests.post(self._endpoint, json=data, headers=headers)

            # Get the response data
            response_data = response.json()
            # Extract the completion text from the response
            if 'choices' in response_data:
                # Access the 'choices' key here
                try:
                    response_dict = json.loads(response_data['choices'][0]['message']['content'])
                except json.decoder.JSONDecodeError as e:
                    print(f"{Fore.RED}error when loading json: {e}{Style.RESET_ALL}")
                    return
            else:
                print(f"{Fore.YELLOW}empty choices in response: {response_data}{Style.RESET_ALL}")
                return

            try:
                if 'main_body' and 'caption' in response_dict:
                    title, body = response_dict
                    return {'title': response_dict[title], 'body': response_dict[body]}
                else:
                    print(f"{Fore.YELLOW}response_dict: {response_dict}{Style.RESET_ALL}")
                    return
            except Exception as e:
                print(f"{Fore.RED}error: {e}{Style.RESET_ALL}")
                return

        except requests.RequestException as e:
            print(f"{Fore.RED}chatgpt: {e}{Style.RESET_ALL}")
            return
