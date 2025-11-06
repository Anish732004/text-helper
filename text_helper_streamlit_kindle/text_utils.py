# Helper string functions for Text Helper app (extended)
def to_upper(text: str) -> str:
    return text.upper()

def to_lower(text: str) -> str:
    return text.lower()

def strip_text(text: str) -> str:
    return text.strip()

def replace_text(text: str, old: str, new: str) -> str:
    if old == "":
        # nothing to replace
        return text
    return text.replace(old, new)

def count_substring(text: str, sub: str) -> int:
    if sub == "":
        return 0
    return text.count(sub)

def word_count(text: str) -> int:
    # naive word count splitting on whitespace
    return len(text.split())

def capitalize_text(text: str) -> str:
    # Capitalize the first non-space character of the entire text
    if not text:
        return text
    for i, ch in enumerate(text):
        if not ch.isspace():
            return text[:i] + text[i].upper() + text[i+1:]
    return text

def title_text(text: str) -> str:
    return text.title()
