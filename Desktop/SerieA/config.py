# config.py

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

GEMINI_MODEL = "gemini-2.5-flash-lite"
GEMINI_TEMPERATURE = 0.2