import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY missing in .env")
if not SERPAPI_API_KEY:
    raise ValueError("❌ SERPAPI_API_KEY missing in .env")

genai.configure(api_key=GEMINI_API_KEY)
