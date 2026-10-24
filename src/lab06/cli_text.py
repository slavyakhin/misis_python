'''
CLI text utility.

Usage:
    python3 cli_text.py <subcommand> [args...]

Available subcommands:
    cat --input <path> [-n]         return file contents line by line (numerated with -n)
    stats --input <txt> [--top 5]   analyze token frequency
'''

import argparse
from pathlib import Path
from src.lab04.io_txt_csv import read_text
from src.lab03.text_stats import print_stats

def main():
    '''
    cli text utility
    '''

    parser = argparse.ArgumentParser(description="cli text utility")
    subparsers = parser.add_subparsers(dest="subcommand")

    # cat
    cat_parser = subparsers.add_parser("cat", help="Print file contents")
    cat_parser.add_argument("--input", required=True)
    cat_parser.add_argument("-n", action="store_true", help="numerate lines")

    # stats
    stats_parser = subparsers.add_parser("stats", help="Tokens frequencies")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args()

    # python 3.10+
    match args.subcommand:
        case "cat":
            input_path = Path(args.input)
            s = read_text(input_path)
            if args.n:
                for i, s in enumerate(s.split('\n')):
                    print(f'{i+1}. {s}')
            else:
                print(s)

        case "stats":
            input_path = Path(args.input)
            input_str = read_text(input_path)
            print_stats(input_str, top=args.top)


if __name__ == "__main__":
    main()
