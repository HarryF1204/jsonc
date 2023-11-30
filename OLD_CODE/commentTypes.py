import string


class _SLComment:
    def __init__(self, value, inline):
        self._value = value
        self._inl = inline
        self._nlChar = '\n'

    def __repr__(self):
        return f'{self._nlChar if self._inl == False else ""}// {self._value}'

    def __str__(self):
        return f'{self._nlChar if self._inl == False else ""}// {self._value}'
