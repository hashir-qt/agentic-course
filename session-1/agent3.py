from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal

client = OpenAI()

class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    reasoning: str

def classify(text: str) -> SentimentResult:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You classify customer messages."},
            {"role": "user", "content": text}
        ],
        response_format=SentimentResult
    )
    return response.choices[0].message.parsed

result = classify("Im not sure about this product")
print(result.sentiment, result.confidence, result.reasoning)