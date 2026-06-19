import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free").strip()

MAX_CLAIMS = int(os.getenv("MAX_CLAIMS", "5"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "8000"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
VERDICT_BADGE = {"Verified": "✅", "Inaccurate": "⚠️", "False": "❌", "Error": "🚫"}