from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Give one short tip for improving a fresher resume."
        }
    ]
)

print(response.choices[0].message.content)