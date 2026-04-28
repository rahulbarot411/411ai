TEMPLATES = {
    "explanation": "You are an expert assistant. Give concise explanation with steps and caveats.",
    "code_generation": "Generate production-ready code. Include file names, commands, and tests.",
    "debugging": "Diagnose likely root causes. Provide reproducible checks then fixes.",
    "infra": "Focus on infra reliability, cost, security, and rollout strategy.",
}

def select_template(user_input: str) -> str:
    low = user_input.lower()
    if any(k in low for k in ["bug", "error", "trace", "fail"]):
        return TEMPLATES["debugging"]
    if any(k in low for k in ["terraform", "kubernetes", "docker", "infra"]):
        return TEMPLATES["infra"]
    if any(k in low for k in ["write code", "implement", "function", "script"]):
        return TEMPLATES["code_generation"]
    return TEMPLATES["explanation"]
