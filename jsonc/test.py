"""This file is to be ignored"""




import re
import string





class JsonC:
    def __init__(self):


        self._jsonCData = ""



    @staticmethod
    def _decodeComments(match) -> str:
        commentContent = match.group(1)
        isInline = match.group(2)
        commentBefore = match.group(3)
        commentContent = str(',' if commentBefore else '') + (
            " " if isInline == 'true' else "\n") + commentContent.replace('\\n', '\n')

        return commentContent



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
