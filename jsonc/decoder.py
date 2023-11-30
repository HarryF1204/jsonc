import re


class _JsonCDecoder:
    def __init__(self):
        self._encodeCommentPattern = re.compile(
            r'(//.*?(\n|$))'        # Match single-line comments (//) until newline or end of string
            r'|'                    # OR
            r'(/\*.*?\*/)',         # Match multi-line comments (/* */) non-greedy
            re.DOTALL | re.MULTILINE
        )


_jsonCDecoder = _JsonCDecoder()
