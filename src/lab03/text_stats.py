import sys
from src.lib.text import normalize, tokenize, count_freq, top_n

N = 5

def main():
    '''
    Read input until EOF, print stats
    '''

    tokens = list()
    for line in sys.stdin:
        tokens.extend(tokenize(normalize(line)))

    freq = count_freq(tokens)
    table = top_n(freq, n=N)

    print(f'Всего слов: {len(tokens)}')
    print(f'Уникальных слов: {len(freq)}')

    print("Топ-5:")
    for pair in table:
        print(f'{pair[0]}:{pair[1]}')


if __name__ == "__main__":
    main()
