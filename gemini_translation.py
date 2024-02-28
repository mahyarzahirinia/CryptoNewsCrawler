import pathlib
import textwrap
import google.generativeai as genai
from colorama import Fore, Style

from IPython.display import display
from IPython.display import Markdown


from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# to this date, gemini doesnt provide content to persian
def translate(text, target_language="Deutsch", except_following="urls"):
    try:
        response = model.generate_content(
            f"Translate the following text to {target_language} except the {except_following}"
            f"and maintain the formatted string intact please:"
            f"{text}")
        return response.text
    except Exception as e:
        raise Exception(f"{Fore.RED}{e}{Style.RESET_ALL}")
