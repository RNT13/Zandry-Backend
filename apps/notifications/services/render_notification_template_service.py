def render_template(text: str, context: dict) -> str:
    class SafeDict(dict):
        def __missing__(self, key):
            return ""

    return text.format_map(SafeDict(**context))
