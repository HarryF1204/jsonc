import re
from ._textUtils import getNonWhitespaceChar, getPrevBracket
from collections import deque


class _JsonCEncoder:

    def __init__(self):
        self._encodeCommentPattern = re.compile(
            r'(//.*?(\n|$))'  # Match single-line comments (//) until newline or end of string
            r'|'  # OR
            r'(/\*.*?\*/)',  # Match multi-line comments (/* */) non-greedy
            re.DOTALL | re.MULTILINE
        )
        self._doubleCommaPatten = re.compile(
            r'(,\s*,)',
            re.DOTALL | re.MULTILINE)
        self._removeComments = re.compile(
            r'(//[^\n]*)|(/\*.*?\*/)',
            re.DOTALL | re.MULTILINE
        )
        self._jsonCData = ""

    def JsonCToJson(self, jsonCData) -> str:
        def isInsideArray(index) -> str | None:
            stack = deque()

            rev_data = self._jsonCData[:index]
            rev_data = self._removeComments.sub('', rev_data)[::-1]  # Incase there is any JSON in the comments

            isInString = False
            for char in rev_data:
                if char == '"':
                    isInString = not isInString
                if char in (']', '}') and not isInString:
                    stack.append(char)
                elif char in ('[', '{') and not isInString:
                    if not stack:
                        return char

                    stack.pop()
            return None

        def encodeComments(match) -> str:
            nextChar = getNonWhitespaceChar(self._jsonCData, match.end())
            prevChar = getNonWhitespaceChar(self._jsonCData, match.start(), reverse=True)
            prevSlChar = getNonWhitespaceChar(self._jsonCData, match.start(), reverse=True, singleLine=True)

            isInline = True if prevSlChar in {',', '"', ']', '}'} else False
            isCommaBefore = True if prevChar != ',' else False
            isCommaAfter = True if nextChar not in {',', ']', '}'} else False

            isInArray = isInsideArray(match.start())
            isInArray = True if isInArray == '[' else False

            commentId = f'{match.start()}_{match.end()}'
            commentContent = match.group().replace('\n', '\\n').replace('\t', '\\t').replace('"', "'")

            finalString = ''.join([
                f'{"," if isCommaBefore else ""}',
                f'"__comment_{commentId}":' if not isInArray else '',
                '{"__comment_content": ',
                f'"{commentContent}",',
                '"__is_inline": ',
                str(str(isInline).lower()),
                '}' if isInArray else '}',
                f'{"," if isCommaAfter else ""}'
            ])

            return finalString

        self._jsonCData = jsonCData.strip("''")
        jsonData = self._encodeCommentPattern.sub(encodeComments, self._jsonCData)
        jsonData = self._doubleCommaPatten.sub(',', jsonData)

        return jsonData
