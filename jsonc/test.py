import re
import string


def _getNonWhitespaceChar(check_string, index, reverse=False, singleLine=False) -> str:
    whitespaceChars = string.whitespace if singleLine is False else {' ', '\t'}
    try:
        if reverse:
            return next(char for char in reversed(check_string[:index]) if char not in whitespaceChars)
        else:
            return next(char for char in check_string[index:] if char not in whitespaceChars)
    except StopIteration:
        return ""


class JsonC:
    def __init__(self):
        self._encodeCommentPattern = re.compile(r'(//.*?(\n|$))|(/\*.*?\*/)', re.DOTALL | re.MULTILINE)
        self._decodeCommentPattern = re.compile(
            r',?\s*"__comment_\d+_\d+":\s*{[^{}]*"__comment_content":\s*"([^"]*)"[^{}]*"__is_inline":\s*(true|false)[^{}]*}\s*(?=\s*[,}])(,?)')
        self._jsonCData = ""

    def _encodeComments(self, match) -> str:
        nextChar = _getNonWhitespaceChar(self._jsonCData, match.end())
        prevChar = _getNonWhitespaceChar(self._jsonCData, match.start(), reverse=True)
        prevSlChar = _getNonWhitespaceChar(self._jsonCData, match.start(), reverse=True, singleLine=True)

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

    @staticmethod
    def _decodeComments(match) -> str:
        commentContent = match.group(1)
        isInline = match.group(2)
        commentBefore = match.group(3)
        commentContent = str(',' if commentBefore else '') + (
            " " if isInline == 'true' else "\n") + commentContent.replace('\\n', '\n')

        return commentContent

    def JsonCToJson(self, jsonCData) -> str:
        self._jsonCData = jsonCData.strip("''")
        jsonData = self._encodeCommentPattern.sub(self._encodeComments, self._jsonCData)
        print(jsonData)
        return jsonData

    def JsonToJsonc(self, jsonCData):
        self._jsonCData = self._decodeCommentPattern.sub(self._decodeComments,
                                                         jsonCData.replace('\n', '').replace('    ', ''))
        return self._jsonCBeautifier()

    @staticmethod
    def _parseMLComments(jsonData, index, tabbing, tabWidth) -> str:
        endIndex = None
        prevChar = ""

        for i, char in enumerate(jsonData[index - 1:]):
            if char == '/' and prevChar == '*':
                endIndex = i + index
            prevChar = char
        if endIndex:
            tab = '\n' + ' ' * tabbing * tabWidth
            return jsonData[index - 1:endIndex].replace('\\n', tab).replace('/*', tab + '/*') + '\n' + tab

    def _jsonCBeautifier(self) -> str:
        inSComment = False
        inMComment = False
        inComment = False
        inArray = False
        inStr = False
        tabbing = 0
        tabWidth = 4
        finalString = ""
        prevChar = ""
        tabNextChar = False
        jsonData = self._jsonCData.__repr__().strip("''")

        for index, char in enumerate(jsonData):
            if tabNextChar is True and _getNonWhitespaceChar(jsonData, index) != '}':
                finalString += '\n' + ' ' * tabbing * tabWidth
                tabNextChar = False
            if inSComment is True:
                if char == ',' or (char == 'n' and prevChar == '\\'):
                    inSComment = False
                    inComment = False
                    tabNextChar = True
            if inMComment is True:
                if char == '/' and prevChar == '*':
                    inComment = False
                    inMComment = False
                else:
                    continue
            if inComment is False:
                if char == '/' and prevChar == '/':
                    inSComment = True
                    inComment = True
                    prevNonWsChar = _getNonWhitespaceChar(jsonData, index - 1, reverse=True)
                    finalString += str(' ' * tabbing * tabWidth if prevNonWsChar == 'n' else '') + '//'
                elif char == '*' and prevChar == '/':
                    finalString += self._parseMLComments(jsonData, index, tabbing, tabWidth)
                    inMComment = True
                    inSComment = False
            if inComment is False:
                if char == '"' and inStr is False:
                    inStr = True
                elif char == '"' and inStr is True:
                    inStr = False

                if inStr is False:
                    if char == '[':
                        inArray = True
                    if char == ']':
                        inArray = False

                    if inArray is False:
                        if char == ',':
                            if _getNonWhitespaceChar(jsonData, index + 3) != '/':
                                char += '\n' + ' ' * tabWidth * tabbing
                    if char == '{':
                        tabbing += 1
                        char += '\n' + ' ' * tabWidth * tabbing
                    elif char == '}':
                        tabbing -= 1
                        char = '\n' + ' ' * tabWidth * tabbing + char

            prevChar = char
            if char != '/' and char != "*":
                finalString += char

        print(finalString.replace('\\n', '\n').replace('\n\n', '\n'))
        return finalString.replace('\\n', '\n').replace('\n\n', '\n')
