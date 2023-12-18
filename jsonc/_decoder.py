import re
from ._textUtils import getNonWhitespaceChar


class _JsonCDecoder:
    def __init__(self):
        self._jsonCData = ""
        self._decodeCommentPattern = re.compile(
            r',?\s*'  # Optional comma and optional whitespace
            r'"(?: __comment_\d+_\d+":\s*)?'  # "__comment_" followed by digits and colon, optional whitespace
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
        self._formatEmptyObjects = re.compile(
            r'(?<=\{)'  # Possitive look behind for opening brace
            r'\s*'      # Whitespace
            r'(?=})'    # Positive look ahead for closing brace
            r'|'        # OR
            r'(?<=\[)'  # Positive look behind for opening bracket
            r'\s*'      # Whitespace
            r'(?=])'    # Positive look ahead for closing bracket
        )

    def JsonToJsonC(self, jsonCData, tabwidth=2):
        def decodeComments(match) -> str:
            commentContent = match.group(1)
            isInline = match.group(2)
            commentBefore = match.group(3)
            commentContent = str(',' if commentBefore else '') + (
                " " if isInline == 'true' else "\n") + commentContent.replace('\\n', '\n')

            return commentContent

        self._jsonCData = jsonCData
        self._jsonCData = self._decodeCommentPattern.sub(decodeComments,
                                                         jsonCData.replace('\n', '').replace('    ', ''))

        return self._jsonCBeautifier(tabwidth)

    def _jsonCBeautifier(self, tabWidth) -> str:
        def parseMLComments(data, j, curr_tabbing, tab_width) -> str:
            endIndex = None
            prev_char = ""

            for i, character in enumerate(data[j - 1:]):
                if character == '/' and prev_char == '*':
                    endIndex = i + j
                prev_char = character
            if endIndex:
                tab = '\n' + ' ' * curr_tabbing * tab_width
                return data[j - 1:endIndex].replace('\\n', tab).replace('/*', tab + '/*') + '\n' + tab

        def spaces(curr_tabbing, tab_width) -> str:
            return ' ' * curr_tabbing * tab_width

        inSComment = False
        inMComment = False
        inComment = False
        inArray = False
        inStr = False
        tabbing = 0
        finalString = ""
        prevChar = ""
        tabNextChar = False
        jsonData = self._jsonCData.__repr__().strip("''")

        for index, char in enumerate(jsonData):
            if tabNextChar is True and getNonWhitespaceChar(jsonData, index) != '}':
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
                    prevNonWsChar = getNonWhitespaceChar(jsonData, index - 1, reverse=True)
                    finalString += str(' ' * tabbing * tabWidth if prevNonWsChar == 'n' else '') + '//'
                elif char == '*' and prevChar == '/':
                    finalString += parseMLComments(jsonData, index, tabbing, tabWidth)
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
                            if getNonWhitespaceChar(jsonData, index + 3) != '/':
                                char += '\n' + spaces(tabbing, tabWidth)
                    if char == '{':
                        tabbing += 1
                        char += '\n' + spaces(tabbing, tabWidth)
                    elif char == '}':
                        tabbing -= 1
                        char = '\n' + spaces(tabbing, tabWidth) + char

            prevChar = char
            if char != '/' and char != "*":
                finalString += char

        finalString = self._formatEmptyObjects.sub('', finalString)
        finalString = finalString.replace('\\n', '\n').replace('\n\n', '\n')

        return finalString
