from re import findall
from src.lib.merge_sort import merge_sorted

TOKEN_PATTERN = r'\w+(?:-\w)*'

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    '''
    Return normalized string.\n
    Remove case distinctions (casefold() by default, else - lower())\n
    Replace 'ё' by 'е'\n
    Erase all whitespace non-standart characters (split(): '\t', '\n', '\r', '\v', '\f').\n
    Collapse all space sequences.\n
    '''

    if not isinstance(text, str):
        raise TypeError("text must be string")
    if not isinstance(casefold, bool):
        raise TypeError("casefold must be bool")
    if not isinstance(yo2e, bool):
        raise TypeError("yo2e must be bool")

    if casefold:
        text = text.casefold()
    else:
        text = text.lower()

    if yo2e:
        text = text.replace('ё', 'е')

    text = ' '.join(text.split())

    return text


def tokenize(text: str) -> list[str]:
    '''
    Return list of substrings that mathes pattern "\\w+(?:-\\w+)*"

    Uses re.findall()
    '''

    if not isinstance(text, str):
        raise TypeError("text must be string")

    tokens = findall(TOKEN_PATTERN, text)

    return tokens


def count_freq(tokens: list[str]) -> dict[str, int]:
    '''
    Return dictionary token -> n occurrences
    '''

    if not isinstance(tokens, list):
        raise TypeError("tokens must be list")
    if not all(isinstance(x, str) for x in tokens):
        raise TypeError("all tokens must be strings")

    freqs = dict()

    for token in tokens:
        freqs[token] = freqs.get(token, 0) + 1

    return freqs


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    '''
    Return top n tokens by descending frequency.

    If equal freq, dictionary order.

    Uses heapq
    '''

    if not isinstance(freq, dict):
        raise TypeError("freq must be dict")
    if not all(isinstance(key, str) and isinstance(value, int) for key, value in freq.items()):
        raise TypeError("freq pairs must be [str, int]")

    top_list = list(freq.items())

    top_list = merge_sorted(top_list, key=lambda x: (x[1], x[0]), reverse=True)

    return top_list[:n]
