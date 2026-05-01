# llm/client.py

import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMPERATURE

genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel(GEMINI_MODEL)


def generate_completion(prompt: str) -> str:
    response = _model.generate_content(
        prompt,
        generation_config={
            "temperature": GEMINI_TEMPERATURE
        }
    )

    return response.text
