from monitoring import monitor_llm_call
from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

@monitor_llm_call
def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()