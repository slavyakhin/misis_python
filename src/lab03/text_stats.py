import sys, os
from src.lib.text import normalize, tokenize, count_freq, top_n

N = 5
MIN_WORD_COL_WIDTH = 5 # len("слово") + how much as you want
DIVIDER_WIDTH = 3 # len(" | ")
FREQ_COL_WIDTH = 7 # len("частота")

def pretty_output(table: list[tuple[str, int]]) -> None:
    '''
    Print pretty formatted table
    '''
    word_col_width = len( max(table, key= lambda x: len(x[0]))[0] )
    word_col_width = max(MIN_WORD_COL_WIDTH, word_col_width)
    table_width = word_col_width + DIVIDER_WIDTH + FREQ_COL_WIDTH

    print(f'{"слово":<{word_col_width}}{"|":^{DIVIDER_WIDTH}}{"Частота":<{FREQ_COL_WIDTH}}')
    print('-' * table_width)

    for pair in table:
        print(f'{pair[0]:<{word_col_width}}{"|":^{DIVIDER_WIDTH}}{pair[1]:<{FREQ_COL_WIDTH}}')
 

def main():
    '''
    Read input until EOF, print stats
    '''

    pretty_flag_str = os.environ.get("PRETTY", default="True")
    pretty_flag =  pretty_flag_str.casefold() in ["true", 'yes', 'y', '1', 't']

    tokens = list()
    for line in sys.stdin:
        tokens.extend(tokenize(normalize(line)))

    freq = count_freq(tokens)
    table = top_n(freq, n=N)

    print(f'Всего слов: {len(tokens)}')
    print(f'Уникальных слов: {len(freq)}')

    if pretty_flag:
        pretty_output(table)
    else:
        print("Топ-5:")
        for pair in table:
            print(f'{pair[0]}:{pair[1]}')


if __name__ == "__main__":
    main()
