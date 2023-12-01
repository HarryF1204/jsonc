import string
import re


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


# Public Dictionary of replacements for escape characters
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}

# Public regex for \ and all non-printable characters
ESCAPE_ASCII = re.compile(r'([\\"]|[^ -~])')


def py_encode_basestring_ascii(s):
    def replace(match):
        s = match.group(0)
        try:
            return ESCAPE_DCT[s]
        except KeyError:
            n = ord(s)
            if n < 0x10000:
                return '\\u{0:04x}'.format(n)
            else:
                # surrogate pair
                n -= 0x10000
                s1 = 0xd800 | ((n >> 10) & 0x3ff)
                s2 = 0xdc00 | (n & 0x3ff)
                return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)

    return '"' + ESCAPE_ASCII.sub(replace, s) + '"'
