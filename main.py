import string
from typing import Union

import textUtils

from commentTypes import _SLComment

jsonc = '''{"test":"test", //test 
"test2": 12345, "test3": 123.095, "test4": [{"test": "test"},{"test": "test"}]}'''


class jsonParser:

    def __init__(self):
        self._setup()

    def _setup(self, jsonData="") -> None:
        self.jsonData = jsonData
        self.index = -1
        self.currentChar = None
        self._advance()

    def _advance(self, index=1) -> None:
        self.index += index
        self.currentChar = self.jsonData[self.index] if self.index < len(self.jsonData) else None

    def _parseNum(self) -> Union[int, float]:
        startIndex = self.index

        while self.currentChar is not None:
            if self.currentChar in (',', string.whitespace, '}', ']'):
                value = self.jsonData[startIndex:self.index]
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            self._advance()
        raise ValueError("Cannot parse value in _parseNum")

    def _parseString(self) -> str:
        self._advance()

        startIndex = self.index
        while self.currentChar is not None:
            if self.currentChar == '"':
                return self.jsonData[startIndex:self.index]
            self._advance()
        raise ValueError(f"Cannot parse value: {self.jsonData[startIndex:self.index]} in _parseString")

    def _parseSLComment(self) -> _SLComment:
        self._advance(2)
        startIndex = self.index
        inline = True

        while self.currentChar is not None:
            if (self.currentChar == '\\' and self.jsonData
            [self.index + 1] == 'n') or self.currentChar == '}' or self.currentChar == ']':
                if textUtils.getNonWhitespaceChar(self.jsonData, startIndex, reverse=True) == 'n':
                    inline = False
                return _SLComment(self.jsonData[startIndex:self.index], inline)
            self._advance()

    def _parseArray(self) -> list:
        self._advance()
        arr = []

        while self.currentChar is not None:
            if self.currentChar == '"':
                arr.append(self._parseValue())
            elif self.currentChar == '{':
                arr.append(self._parseObject())
            elif self.currentChar in string.digits:
                arr.append(self._parseNum())
            elif self.currentChar == '/' and self.jsonData[self.inde x + 1] == '/':
                arr.append(self._parseSLComment())
            elif self.currentChar == ']':
                return arr
            self._advance()

    def _parseValue(self) -> dict:
        self._advance()

        key = None
        value = None
        startIndex = self.index

        while self.currentChar is not None:
            if key is None:
                if self.currentChar == '"':
                    key = self.jsonData[startIndex:self.index]
            elif value is None:
                if self.currentChar == '"':
                    value = self._parseString()
                elif self.currentChar in string.digits:
                    value = self._parseNum()
                elif self.currentChar == '{':
                    value = self._parseObject()
                elif self.currentChar == '[':
                    value = self._parseArray()
                elif self.currentChar == '/':
                    value = self._parseSLComment()
            if key is not None and value is not None:
                return {key: value}
            self._advance()
        raise ValueError(f"Cannot parse value: {self.jsonData[startIndex:self.index]} in _parseValue")

    def _parseObject(self) -> dict:
        finalDict = {}

        while self.currentChar is not None:
            if self.currentChar == '/' and self.jsonData[self.inde x + 1] == '/':
                finalDict.update({f'__comment_{self.index}': self._parseSLComment()})
            if self.currentChar == '"':
                newValue = self._parseValue()
                finalDict.update(newValue)
            if self.currentChar == '}':
                return finalDict
            self._advance()
        pass

    def parseJson(self, jsonStr) -> dict:
        self._setup(jsonStr.__repr__().strip("''"))
        print(self.jsonData)
        finalDict = {}

        while self.currentChar is not None:
            if self.currentChar == '{':
                obj = self._parseObject()
                finalDict.update(obj)
            if self.currentChar == '}':
                return finalDict

            self._advance()


parser = jsonParser()
print(parser.parseJson(jsonc))
