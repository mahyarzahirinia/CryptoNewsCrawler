from openai import OpenAI
from config import chatgpt_token


class ChatGPTTranslator:
    def __init__(self):
        self.client = OpenAI(api_key=chatgpt_token)

    def translate(self, text, target_language="Persian", except_following="urls"):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": f"Translate the following text to {target_language} except the {except_following} "
                            f"and maintain the formatted string intact please."},
                {"role": "user", "content": text}
            ]
        )
        print(response.choices[0].message.content)
