""" Generate numbers dataset
"""

import argparse, random
from pathlib import Path
from src.lab04.io_txt_csv import write_csv

DEFAULT_SEED = 42
HEADER = "value", # tuple
DEFAULT_MIN = -2147483648 # - 2 ** 31
DEFAULT_MAX = 2147483647 # 2 ** 31 - 1
DEFAULT_DIR_PATH="data/numbers"

SMALL_SIZE = 1_000
MEDIUM_SIZE = 10_000
LARGE_SIZE = 100_000

def generate(
    n: int,
    seed: int = DEFAULT_SEED,
    min_value=DEFAULT_MIN,
    max_value=DEFAULT_MAX,
    out_dir=DEFAULT_DIR_PATH,
) -> None:
    """
    write n ints to values_{n:_}.csv
    """

    random.seed(seed)

    out_path = Path(out_dir) / f"values_{n:_}.csv"

    write_csv([(random.randint(min_value, max_value),) for _ in range(n)], out_path , header=HEADER)


def main():
    parser = argparse.ArgumentParser(description="generate numbers.csv dataset")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-n", type=int, help="number of ints")
    group.add_argument("--all", "-a", dest="all_flag", action="store_true", help="generate set csv's")

    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="number of ints")
    parser.add_argument("--min", type=int, default=DEFAULT_MIN, help="min value")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX, help="max value")
    parser.add_argument("--out", default=DEFAULT_DIR_PATH, help="output dir path")
    
    args = parser.parse_args()

    if args.all_flag:
        generate(n=SMALL_SIZE, seed=args.seed, min_value=args.min, max_value=args.max, out_dir=args.out)
        generate(n=MEDIUM_SIZE, seed=args.seed, min_value=args.min, max_value=args.max, out_dir=args.out)
        generate(n=LARGE_SIZE, seed=args.seed, min_value=args.min, max_value=args.max, out_dir=args.out)
    else:
        generate(n=args.n, seed=args.seed, min_value=args.min, max_value=args.max, out_dir=args.out)


if __name__ == "__main__":
    main()
