import ollama

ROUTER_MODEL = "gemma3:1b"

ROUTER_PROMPT = """Classify this request with ONE word only.

Rules:
- simple: greetings, small talk, yes/no questions
- code: write code, fix bug, script, programming, debug, function, class
- normal: explain concept, summarize, translate, general question
- advanced: complex analysis, architecture, deep reasoning

Request: {query}

Reply with ONE word (simple/code/normal/advanced):"""

MODEL_MAP = {
    "simple":   "gemma3:1b",
    "normal":   "gemma4",
    "advanced": "qwen2.5:32b",
    "code":     "deepseek-coder-v2",
}

FALLBACK_MODEL = "gemma4"


def route(user_input: str) -> str:
    """Choisit le bon modèle selon la complexité de la requête."""
    prompt = ROUTER_PROMPT.format(query=user_input)
    response = ollama.chat(
        model=ROUTER_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    category = response["message"]["content"].strip().lower().split()[0]
    return MODEL_MAP.get(category, FALLBACK_MODEL)
