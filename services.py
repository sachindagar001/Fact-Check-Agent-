import requests
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from tavily import TavilyClient
import config

class TransientError(Exception):
    pass

def _retryable(sc): 
    return sc in (408, 425, 429, 500, 502, 503, 504)

@st.cache_resource
def get_tavily_client():
    return TavilyClient(api_key=config.TAVILY_API_KEY)

@st.cache_resource
def get_openrouter_headers():
    return {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost/fact-check-agent",
        "X-Title": "Fact-Check Agent",
    }

@retry(
    retry=retry_if_exception_type((requests.exceptions.RequestException, TransientError, ValueError)),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(4),
    reraise=True,
)
def call_llm(prompt: str) -> str:
    resp = requests.post(
        config.OPENROUTER_URL,
        headers=get_openrouter_headers(),
        json={"model": config.OPENROUTER_MODEL, "messages": [{"role": "user", "content": prompt}]},
        timeout=90
    )
    if resp.status_code >= 400:
        err = requests.exceptions.HTTPError(f"HTTP {resp.status_code}: {resp.text[:200]}", response=resp)
        if _retryable(resp.status_code): raise err
        raise err
    try: 
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e: 
        raise TransientError(f"Bad payload: {resp.text[:200]}") from e

@retry(
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(4),
    reraise=True,
)
def search_web(query: str) -> dict:
    return get_tavily_client().search(query=query, search_depth="advanced", max_results=config.MAX_SEARCH_RESULTS)