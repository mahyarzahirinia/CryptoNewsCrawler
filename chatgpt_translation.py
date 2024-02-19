from openai import OpenAI
from config import chatgpt_token

from colorama import Fore, Style


class ChatGPTTranslator:
    def __init__(self):
        self.client = OpenAI(api_key=chatgpt_token)

    def translate(self, text, target_language="Persian", except_following="urls"):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system",
                     "content": f"Translate the following text to {target_language} except the {except_following} "
                                f"and maintain the formatted string intact please."},
                    {"role": "user", "content": text}
                ]
            )
            print("test")
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"{Fore.RED}{e}{Style.RESET_ALL}")