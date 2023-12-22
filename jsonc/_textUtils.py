import string


def getNonWhitespaceChar(check_string, index, reverse=False, singleLine=False) -> str:
    whitespaceChars = string.whitespace if singleLine is False else (' ', '\t')
    try:
        if reverse:
            return next(char for char in reversed(check_string[:index]) if char not in whitespaceChars)
        else:
            return next(char for char in check_string[index:] if char not in whitespaceChars)
    except StopIteration as e:
        print('Stop iteration error', e)
        return ""
    except IndexError as e:
        print('List index out of range: ', e)
        return ""


def getPrevBracket(check_string, index):
    try:
        return next(char for char in check_string[index:] if char not in ('[', '{'))

    except StopIteration as e:
        print('Stop iteration error', e)
        return ""
    except IndexError as e:
        print('List index out of range: ', e)
        return ""