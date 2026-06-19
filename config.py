import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_config(key, default=""):
    # 1. Check Streamlit Cloud secrets first
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key].strip()
    except Exception:
        pass
    
    # 2. Fall back to local .env file
    return os.getenv(key, default).strip()

TAVILY_API_KEY = get_config("TAVILY_API_KEY")
OPENROUTER_API_KEY = get_config("OPENROUTER_API_KEY")
OPENROUTER_MODEL = get_config("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")

MAX_CLAIMS = int(get_config("MAX_CLAIMS", "5"))
MAX_CONTEXT_CHARS = int(get_config("MAX_CONTEXT_CHARS", "8000"))
MAX_SEARCH_RESULTS = int(get_config("MAX_SEARCH_RESULTS", "5"))

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
VERDICT_BADGE = {"Verified": "✅", "Inaccurate": "⚠️", "False": "❌", "Error": "🚫"}
