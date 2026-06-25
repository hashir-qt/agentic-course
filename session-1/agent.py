from openai import OpenAI

client = OpenAI

response = client.chat.completions.create(
    model="gpt-40-mini",
    messages=[{"role": "user", "content": "say hello in three languages"}]
)

print(response.choice[0].message.content)