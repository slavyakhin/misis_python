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
    if table:
        word_col_width = len( max(table, key= lambda x: len(x[0]))[0] )
        word_col_width = max(MIN_WORD_COL_WIDTH, word_col_width)
    else:
        # Empty table
        word_col_width = MIN_WORD_COL_WIDTH
    table_width = word_col_width + DIVIDER_WIDTH + FREQ_COL_WIDTH

    print(f'{"Cлово":<{word_col_width}}{"|":^{DIVIDER_WIDTH}}{"Частота":<{FREQ_COL_WIDTH}}')
    print('-' * table_width)

    for pair in table:
        print(f'{pair[0]:<{word_col_width}}{"|":^{DIVIDER_WIDTH}}{pair[1]:<{FREQ_COL_WIDTH}}')
 

def print_summary(total_tokens: int, unique_tokens: int, table: list[tuple | list], pretty: bool = True):
    '''
    Print summary
    '''
 
    print(f'Всего слов: {total_tokens}')
    print(f'Уникальных слов: {unique_tokens}')

    if pretty:
        pretty_output(table)
    else:
        print(f"Топ-{len(table)}:")
        for pair in table:
            print(f'{pair[0]}:{pair[1]}')   


def print_stats(input_str: str, top: int = N, pretty: bool = True):
    '''
    print stats from string
    '''

    tokens = tokenize(normalize(input_str))
    freq = count_freq(tokens)
    table = top_n(freq, n=top)

    print_summary(total_tokens=len(tokens),
                  unique_tokens=len(freq),
                  table=table,
                  pretty=pretty)


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

    print_summary(total_tokens=len(tokens),
                  unique_tokens=len(freq),
                  table=table,
                  pretty=pretty_flag)

if __name__ == "__main__":
    main()
