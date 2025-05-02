import re

# ---------------------------
# Utility
# ---------------------------
class ResponseCleaner:
    @staticmethod
    def clean(text):
        text = re.sub(r"[*_`#~]", "", text)
        text = re.sub(r"(?<=[a-zA-Z0-9])\n(?=[a-zA-Z0-9])", "", text)
        text = re.sub(r"\n{2,}", "\n\n", text)
        return text.strip()
