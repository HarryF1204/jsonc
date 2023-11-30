import re


class _JsonCDecoder:
    def __init__(self):
        self._decodeCommentPattern = re.compile(
            r',?\s*'  # Optional comma and optional whitespace
            r'"__comment_\d+_\d+":\s*'  # "__comment_" followed by digits and colon, optional whitespace
            r'{[^{}]*'  # Opening curly brace and anything but curly braces inside
            r'"__comment_content":\s*'  # "__comment_content" and optional whitespace
            r'"([^"]*)"'  # Capturing group for content inside double quotes
            r'[^{}]*'  # Anything but curly braces
            r'"__is_inline":\s*'  # "__is_inline" and optional whitespace
            r'(true|false)'  # Capturing group for "true" or "false"
            r'[^{}]*}\s*'  # Anything but braces followed by closing brace and optional whitespace
            r'(?=\s*[,}])'  # Lookahead for optional whitespace and comma or closing curly brace
            r'(,?)'  # Optional comma (captured in a group)
        )


_jsonCDecoder = _JsonCDecoder()
