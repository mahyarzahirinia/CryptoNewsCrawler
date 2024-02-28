from colorama import Fore, Style
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()


class ChatGPTTranslator:
    def __init__(self):
        self.client = OpenAI()
        # api_key=os.environ.get("OPENAI_API_KEY")

    def translate(self, text, target_language="Persian", except_following="urls and numbers"):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "text"},
                messages=[
                    {"role": "system",
                     "content": f"Translate the following text to {target_language} except the {except_following}"
                                f"and maintain the formatted string intact please: \n"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"{Fore.RED}{e}{Style.RESET_ALL}")

    def translate_chunks(self, *args, seperator="\\", target_language="Persian") -> list:
        chunks = ''
        for arg in args:
            chunks += f"{str(arg)}{seperator}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "text"},
                messages=[
                    {"role": "system",
                     "content": f"Translate the following text to {target_language} and keep the {seperator}"},
                    {"role": "user", "content": chunks}
                ]
            )
            translated = response.choices[0].message.content.split(seperator)
            return translated
        except Exception as e:
            raise Exception(f"{Fore.RED}{e}{Style.RESET_ALL}")
