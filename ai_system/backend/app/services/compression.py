def compress_history(messages: list[dict], max_chars: int = 12000) -> str:
    rendered = []
    total = 0
    for m in reversed(messages):
        line = f"{m['role']}: {m['content']}\n"
        total += len(line)
        if total > max_chars:
            break
        rendered.append(line)
    return ''.join(reversed(rendered))
