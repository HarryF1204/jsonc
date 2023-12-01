import re
from jsonc.textUtils import getNonWhitespaceChar


class JsonCEncoder:

    def __init__(self):
        self._encodeCommentPattern = re.compile(
            r'(//.*?(\n|$))'  # Match single-line comments (//) until newline or end of string
            r'|'  # OR
            r'(/\*.*?\*/)',  # Match multi-line comments (/* */) non-greedy
            re.DOTALL | re.MULTILINE
        )
        self._jsonCData = ""

    def JsonCToJson(self, jsonCData) -> str:
        def encodeComments(match) -> str:
            nextChar = getNonWhitespaceChar(self._jsonCData, match.end())
            prevChar = getNonWhitespaceChar(self._jsonCData, match.start(), reverse=True)
            prevSlChar = getNonWhitespaceChar(self._jsonCData, match.start(), reverse=True, singleLine=True)

            isInline = True if prevSlChar in {',', '"', ']', '}'} else False
            isCommaBefore = True if prevChar != ',' else False
            isCommaAfter = True if nextChar not in {',', ']', '}'} else False

            commentId = f'{match.start()}_{match.end()}'
            commentContent = match.group().replace('\n', '\\n')

            finalString = ''.join([
                f'{"," if isCommaBefore else ""}"__comment_{commentId}":',
                '{"__comment_content": ',
                f'"{commentContent}",',
                '"__is_inline": ',
                str(str(isInline).lower()),
                '}',
                f'{"," if isCommaAfter else ""}'
            ])

            return finalString

        self._jsonCData = jsonCData.strip("''")
        jsonData = self._encodeCommentPattern.sub(encodeComments, self._jsonCData)
        return jsonData
