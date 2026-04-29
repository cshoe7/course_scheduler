import os
from ollama import Client

client = Client(
    host="https://ollama.com",
    #an environemnt variable w the API key
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

messages = [
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
]

for part in client.chat('gpt-oss:120b', messages=messages, stream=True):
    print(part['message']['content'], end='', flush=True)
