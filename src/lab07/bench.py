import csv
import timeit
import argparse
import multiprocessing as mp
from multiprocessing.connection import Connection 
from pathlib import Path
import random
from collections.abc import Sequence, Callable
from src.lib.fmt_table import recs_to_rows, print_table
from src.lab04.io_txt_csv import write_csv
from src.lab07.sorting import bubble_sorted, insertion_sorted, selection_sorted, merge_sorted, counting_sorted
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast


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
TWO_SUM_REQUEST_COUNT = 100 # 100


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


def _timeit_worker(
    writer_conn: Connection,
    fn: Callable,
    reqs: Sequence[tuple[tuple, dict]], # Sequence of pairs (args, kwargs)
    number: int,
    repeat: int,
) -> None:
    """
    Subprocess execute target function.
    Call timeit for each test case.
    Put sum of best times in queue.
    """

    with writer_conn: # Close connection automatically
        total_time = 0
        for args, kwargs in reqs:
            times = timeit.repeat(lambda: fn(*args, **kwargs), number=number, repeat=repeat)
            best = min(times) / number
            total_time += best
            
        writer_conn.send(total_time)


def exec_worker_with_timeout(
    worker: Callable,
    args: tuple = (),
    kwargs: dict = {},
    timeout: float | int = TIMEOUT,
):
    """
    Exec fn worker, terminate after timeout exceeds and raise TimeoutError.

    Return value from the pipe
    """

    reader_conn, writer_conn = mp.Pipe(duplex=False)

    process = mp.Process(target=worker, args=(writer_conn, *args), kwargs=kwargs)

    try:
        process.start()
        writer_conn.close()

        if not reader_conn.poll(timeout):
            raise TimeoutError("Timeout exceeded.")

        try:
            result = reader_conn.recv()
        except EOFError:
            raise RuntimeError("Worker process crashed before sending data.")

        return result

    finally:
        reader_conn.close()
        writer_conn.close()

        if process.is_alive():
            process.terminate()
            process.join(timeout=1)

        if process.is_alive():
            process.kill()

        process.join()


def bench(
    fn: Callable,
    reqs: Sequence[tuple[tuple, dict]], # Sequence of pairs (args, kwargs)
    repeat: int = REPEAT,
    number: int = NUMBER,
    timeout: float | int = TIMEOUT,
) -> float | None:
    """
    Benchmark func.
    Return elapsed time.

    If timeout exceeds, returns None.
    """

    try:
        t = exec_worker_with_timeout(
            worker=_timeit_worker,
            kwargs={
                "fn": fn,
                "reqs": reqs,
                "number": number,
                "repeat": repeat
            },
            timeout=timeout
            )
        return t
    except TimeoutError:
        return None


def _fmt_time(t, timeout, spec=".2f") -> str:
    """
    Format time results
    """
    return format(t, spec) if t is not None else f">{timeout}"


def main():
    """
    Benchmark sort, search and two sum algorithms.
    """
    parser = argparse.ArgumentParser(description="Benchmark algorithms")

    parser.add_argument("-t", "--timeout", dest="timeout", type=float, default=TIMEOUT, help="A function tests execution timeout")
    parser.add_argument("-p", "--precision", dest="precision", type=int, default=PRECISION, help="Number of decimal places")

    args = parser.parse_args()

    # Data preparation
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
    linear_search_reqs = [((),
                            {
                               "nums": numbers_l,
                               "x": random.randint(DEFAULT_MIN, DEFAULT_MAX)
                            }
                        ) for _ in range(SEARCH_REQUEST_COUNT)
                    ]

    binary_search_reqs = [((),
                            {
                               "sorted_nums": numbers_sorted_l,
                               "x": kwargs["x"]
                            }
                        ) for _, kwargs in linear_search_reqs
                    ]

    # Two sum requests
    two_sum_reqs_s = [((),
                       {
                           "nums": numbers_s,
                           "target": sum(random.sample(numbers_s, 2))
                       }
                    ) for _ in range(TWO_SUM_REQUEST_COUNT)
                ]

    two_sum_reqs_m = [((),
                       {
                           "nums": numbers_m,
                           "target": sum(random.sample(numbers_m, 2))
                       }
                    ) for _ in range(TWO_SUM_REQUEST_COUNT)
                ]

    two_sum_reqs_l = [((),
                       {
                           "nums": numbers_l,
                           "target": sum(random.sample(numbers_l, 2))
                       }
                    ) for _ in range(TWO_SUM_REQUEST_COUNT)
                ]
    # --------------- Declarative tests ---------------

    # Test table line consists of a function, it's complexity and test cases
    # fn: Callable - the function being tested
    # complexity: str

    # Test case is a dictionary with required keys:
    # "name": str - name of case (e.g. "n=10^3")
    # ----- bench args -----
    # "reqs": list[tuple[tuple, dict]] - list of (arsg, kwargs) requests
    # If "reqs" is missing -> use args, kwargs as the only one request
    # "args": tuple - the function's args
    # "kwargs": dict - the function's kwargs

    # "number": int - timeit number
    # "repeat": int - timeit repeat
    # "timeout": float | int

    tests_table = [

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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 2,
                    "repeat": 2,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 1,
                    "repeat": 1,
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 2,
                    "repeat": 2,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 1,
                    "repeat": 1,
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 2,
                    "repeat": 2,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 1,
                    "repeat": 1,
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "args": (numbers_m,),
                    "number": 5,
                    "repeat": 10,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "args": (numbers_l,),
                    "number": 5,
                    "repeat": 10,
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_m},
                    "number": 5,
                    "repeat": 10,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_l},
                    "number": 5,
                    "repeat": 10,
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "kwargs": {"nums": numbers_limited_m, "lo": LO, "hi": HI},
                    "number": 5,
                    "repeat": 10,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {"nums": numbers_limited_l, "lo": LO, "hi": HI},
                    "number": 5,
                    "repeat": 10,
                    "timeout": args.timeout,
                }
            ],
        },
        
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
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                }
            ]
        },

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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "reqs": two_sum_reqs_m,
                    "number": 1,
                    "repeat": 1,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "reqs": two_sum_reqs_l,
                    "number": 1,
                    "repeat": 1,
                    "timeout": args.timeout,
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
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^4",
                    "reqs": two_sum_reqs_m,
                    "number": 2,
                    "repeat": 3,
                    "timeout": args.timeout,
                },
                {
                    "name": "n=10^5",
                    "reqs": two_sum_reqs_l,
                    "number": 2,
                    "repeat": 2,
                    "timeout": args.timeout,
                }
            ],
        }
   ]

    result_recs = [dict() for _ in range(len(tests_table))]

    for i, line in enumerate(tests_table):
        result_recs[i]["Algorithm"] = line["name"]
        result_recs[i]["Complexity"] = line["complexity"]
        print(f'Benching "{line["name"]}"...')
        for j, case in enumerate(line["cases"]):
            print(f'case {j}: "{case["name"]}"...')
            assert isinstance(case, dict)
            t = bench(
                fn=line["fn"],
                reqs=case.get("reqs") or [(case.get("args", ()), case.get("kwargs", {}))],
                number=case.get("number", NUMBER),
                repeat=case.get("repeat", REPEAT),
                timeout=case.get("timeout", args.timeout),
            )
            t_str = _fmt_time(t, args.timeout, spec=f".{args.precision}f")
            result_recs[i][case["name"]] = t_str

    rows = recs_to_rows(result_recs)
    print_table(rows)


if __name__ == "__main__":
    main()
