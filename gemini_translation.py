import pathlib
import textwrap
import google.generativeai as genai
from colorama import Fore, Style

# A utility to securely store your API key

from config import gemini_token


class GeminiTranslator:
    def __init__(self):
        self.client = genai.configure(api_key=gemini_token)
        self.model = self.client.GenerativeModel('gemini-pro')

    def translate(self, text, target_language="Persian", except_following="urls"):
        try:
            response = self.model.generate_content(
                f"Translate the following text to {target_language} except the {except_following}"
                f"and maintain the formatted string intact please:"
                f"{text}")
            print("test")
            return response
        except Exception as e:
            raise Exception(f"{Fore.RED}{e}{Style.RESET_ALL}")
