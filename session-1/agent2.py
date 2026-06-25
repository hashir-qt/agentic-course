from openai import OpenAI
client = OpenAI()

SYSTEM = """You classify customer messages.
Return only one word: positive, negative, or neutral."""

def classify(text: str) -> str:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

print(classify("This product is amazing"))
print(classify("Disappointed, returning it"))