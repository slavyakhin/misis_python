import csv
import argparse
import threading
from pathlib import Path
import random
from src.lib.fmt_table import recs_to_rows, print_table
from src.lib.stopwatch import stopwatch_worker
from src.lib.benchmark import start_benchmark
from src.lab04.io_txt_csv import write_csv
from src.lab07.sorting import bubble_sorted, insertion_sorted, selection_sorted, merge_sorted, counting_sorted
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.plot import show_bench_plot


DEFAULT_CSV = "data/lab07/bench.csv"

SEED = 42

DEFAULT_MIN = -2147483648 # - 2 ** 31
DEFAULT_MAX = 2147483647 # 2 ** 31 - 1

TIMEOUT = 60 # Maximum execution time (60 seconds in instruction)
PRECISION = 4 # Number of decimal places

REPEAT = 1
NUMBER = 1

LO = -10_000 # numbers_limited lo
HI = 10_000 # numbers_limited hi

SEARCH_REQUEST_COUNT = 10_000 # 10_000
TWO_SUM_REQUEST_COUNT = 10 # 1


def read_numbers(path: Path) -> list:
    """
    List of numbers
    """
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if headers:
            return [int(row[headers[0]]) for row in reader]
        else:
            return []


def main():
    """
    Benchmark sort, search and two sum algorithms.
    """
    parser = argparse.ArgumentParser(description="Benchmark algorithms")

    parser.add_argument("-t", "--timeout", dest="timeout", type=float, default=TIMEOUT, help="A function tests execution timeout")
    parser.add_argument("-p", "--precision", dest="precision", type=int, default=PRECISION, help="Number of decimal places")
    parser.add_argument("--csv", action="store_true", help="Write results to csv")
    parser.add_argument("--csv-path", dest="csv_str", default=DEFAULT_CSV, help="CSV output path")
    parser.add_argument("--plot", action="store_true", help="Show plot with results")

    args = parser.parse_args()

    # --------------- Data preparation ---------------
    # ! All functions must not make impact on input data

    numbers_s = read_numbers(Path("data/numbers/values_1_000.csv"))
    numbers_m = read_numbers(Path("data/numbers/values_10_000.csv"))
    numbers_l = read_numbers(Path("data/numbers/values_100_000.csv"))

    # Binary search sorted input
    numbers_sorted_l = sorted(numbers_l)

    # Counting sort limited input
    numbers_limited_s = read_numbers(Path("data/numbers_limited/values_1_000.csv"))
    numbers_limited_m = read_numbers(Path("data/numbers_limited/values_10_000.csv"))
    numbers_limited_l = read_numbers(Path("data/numbers_limited/values_100_000.csv"))

    random.seed(SEED)

    # Search requests
    linear_search_reqs = [((), {"nums": numbers_l, "x": random.randint(DEFAULT_MIN, DEFAULT_MAX)})
                          for _ in range(SEARCH_REQUEST_COUNT)]

    binary_search_reqs = [((), {"sorted_nums": numbers_sorted_l, "x": kwargs["x"]})
                          for _, kwargs in linear_search_reqs]

    # Two sum requests
    two_sum_reqs_s = [((), {"nums": numbers_s, "target": sum(random.sample(numbers_s, 2))})
                      for _ in range(TWO_SUM_REQUEST_COUNT)]

    two_sum_reqs_m = [((), {"nums": numbers_m, "target": sum(random.sample(numbers_m, 2))})
                      for _ in range(TWO_SUM_REQUEST_COUNT)]

    two_sum_reqs_l = [((), {"nums": numbers_l, "target": sum(random.sample(numbers_l, 2))})
                      for _ in range(TWO_SUM_REQUEST_COUNT)]

    # --------------- Declarative tests ---------------

    # Test table line consists of a function, it's complexity and test cases
    # "fn": Callable - the function being tested
    # "complexity": str

    # Test case is a dictionary with required keys:
    # "name": str - name of case (e.g. "n=10^3")
    # ----- bench args -----
    # "reqs": list[tuple[tuple, dict]] - list of (args, kwargs) requests
    # If "reqs" is missing -> use args, kwargs as the only one request
    # "args": tuple - the function's args
    # "kwargs": dict - the function's kwargs

    # "number": int - timeit number
    # "repeat": int - timeit repeat
    # "timeout": float | int

    tests_table = []
    sorting_tests = [
        # SORTING
        {
            "name": "Bubble sort",
            "fn": bubble_sorted,
            "complexity": "O(n^2)",
            "cases": [
                {
                    "name": "n=10^3",
                    "kwargs": {"nums": numbers_s},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 2,
                    "repeat": 2,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 1,
                    "repeat": 1,
                }
            ],
        },
        {
            "name": "Insertion sort",
            "fn": insertion_sorted,
            "complexity": "O(n^2)",
            "cases": [
                {
                    "name": "n=10^3",
                    "kwargs": {"nums": numbers_s},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 2,
                    "repeat": 2,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 1,
                    "repeat": 1,
                }
            ],
        },
        {
            "name": "Selection sort",
            "fn": selection_sorted,
            "complexity": "O(n^2)",
            "cases": [
                {
                    "name": "n=10^3",
                    "kwargs": {"nums": numbers_s},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 2,
                    "repeat": 2,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 1,
                    "repeat": 1,
                }
            ],
        },
        {
            "name": "Tim sort",
            "fn": sorted,
            "complexity": "O(n logn)",
            "cases": [
                {
                    "name": "n=10^3",
                    "args": (numbers_s,),
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "args": (numbers_m,),
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "args": (numbers_l,),
                    "number": 5,
                    "repeat": 10,
                }
            ],
        },
        {
            "name": "Merge sort",
            "fn": merge_sorted,
            "complexity": "O(n logn)",
            "cases": [
                {
                    "name": "n=10^3",
                    "kwargs": {"nums": numbers_s},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 5,
                    "repeat": 10,
                }
            ],
        },
        {
            "name": "Counting sort",
            "fn": counting_sorted,
            "complexity": "O(n)",
            "cases": [
                {
                    "name": "n=10^3",
                    "kwargs": {"nums": numbers_limited_s, "lo": LO, "hi": HI},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_limited_m, "lo": LO, "hi": HI},
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_limited_l, "lo": LO, "hi": HI},
                    "number": 5,
                    "repeat": 10,
                }
            ],
        },
    ]

    search_tests = [
        # Search
        {
            "name": "Linear search",
            "fn": linear_search,
            "complexity": "O(n)",
            "cases": [
                {
                    "name": "n=10^5",
                    "reqs": linear_search_reqs,
                    "number": 2,
                    "repeat": 2,
                }
            ]
        },
        {
            "name": "Binary search",
            "fn": binary_search,
            "complexity": "O(n)",
            "cases": [
                {
                    "name": "n=10^5",
                    "reqs": binary_search_reqs,
                    "number": 5,
                    "repeat": 10,
                }
            ]
        },
    ]
    two_sum_tests = [
        # Two sum
        {
            "name": "Two sum brute",
            "fn": two_sum_brute,
            "complexity": "O(n^2)",
            "cases": [
                {
                    "name": "n=10^3",
                    "reqs": two_sum_reqs_s,
                    "number": 1,
                    "repeat": 1,
                },
                {
                    "name": "n=10^4",
                    "reqs": two_sum_reqs_m,
                    "number": 1,
                    "repeat": 1,
                },
                {
                    "name": "n=10^5",
                    "reqs": two_sum_reqs_l,
                    "number": 1,
                    "repeat": 1,
                }
            ],
        },
        {
            "name": "Two sum fast",
            "fn": two_sum_fast,
            "complexity": "O(n)",
            "cases": [
                {
                    "name": "n=10^3",
                    "reqs": two_sum_reqs_s,
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^4",
                    "reqs": two_sum_reqs_m,
                    "number": 2,
                    "repeat": 3,
                },
                {
                    "name": "n=10^5",
                    "reqs": two_sum_reqs_l,
                    "number": 2,
                    "repeat": 2,
                }
            ],
        }
   ]

    tests_table.extend(sorting_tests)
    tests_table.extend(search_tests)
    tests_table.extend(two_sum_tests)

    # Stopwatch thread
    stop_event = threading.Event()
    stopwatch_thread = threading.Thread(target=stopwatch_worker, args=(stop_event,), daemon=True)
    stopwatch_thread.start()

    result_recs = start_benchmark(tests_table, args.timeout, args.precision)

    stop_event.set()
    stopwatch_thread.join()

    rows = recs_to_rows(result_recs)

    print_table(rows)

    if args.csv:
        write_csv(rows, Path(args.csv_str))

    if args.plot:
        show_bench_plot(result_recs)

if __name__ == "__main__":
    main()
