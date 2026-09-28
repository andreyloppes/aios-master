"""AIOS-FORGE - LLM Chat Service"""
import requests
from config import get_key

def chat(prompt, provider=None):
    """Chat with fallback: Groq -> Gemini -> Ollama"""
    if provider == "groq":
        return groq_chat(prompt)
    elif provider == "gemini":
        return gemini_chat(prompt)
    elif provider == "ollama":
        return ollama_chat(prompt)

    result = groq_chat(prompt)
    if not result:
        print("\n  Tentando Gemini...")
        result = gemini_chat(prompt)
    if not result:
        print("\n  Tentando Ollama...")
        result = ollama_chat(prompt)
    return result

def groq_chat(prompt, model="llama-3.3-70b-versatile"):
    """Groq LLM (FREE - 14.4K req/day)"""
    api_key = get_key("groq_api_key", "GROQ_API_KEY")
    if not api_key:
        return None

    print(f"  \033[36m→\033[0m Groq ({model})...")
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 4096},
            timeout=30,
        )
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            print(result)
            return result
    except Exception:
        pass
    return None

def gemini_chat(prompt):
    """Google Gemini chat (FREE)"""
    api_key = get_key("google_api_key", "GOOGLE_API_KEY")
    if not api_key:
        return None

    print(f"  \033[36m→\033[0m Gemini...")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        print(response.text)
        return response.text
    except Exception:
        return None

def ollama_chat(prompt, model="llama3.2"):
    """Ollama local (FREE, UNLIMITED)"""
    print(f"  \033[36m→\033[0m Ollama ({model})...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        if response.status_code == 200:
            result = response.json()["response"]
            print(result)
            return result
    except requests.ConnectionError:
        print("  \033[31m✗\033[0m Ollama nao esta rodando (execute: ollama serve)")
    return None
