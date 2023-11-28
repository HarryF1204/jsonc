import string


def getNonWhitespaceChar(check_string, index, reverse=False, singleLine=False) -> str:
    whitespaceChars = string.whitespace if singleLine is False else {' ', '\t'}
    try:
        if reverse:
            return next(char for char in reversed(check_string[:index]) if char not in whitespaceChars)
        else:
            return next(char for char in check_string[index:] if char not in whitespaceChars)
    except StopIteration:
        return ""
