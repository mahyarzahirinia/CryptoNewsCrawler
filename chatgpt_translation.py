from openai import OpenAI

client = None


def initiate(api_key):
    global client
    client = OpenAI(api_key=api_key)


def translate(text, target_language):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    )
    print(response.choices[0].message.content)
