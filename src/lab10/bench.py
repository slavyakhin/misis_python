import argparse
import threading
from copy import deepcopy
from pathlib import Path
from src.lib.benchmark import start_benchmark
from src.lib.stopwatch import stopwatch_worker
from src.lib.fmt_table import recs_to_rows, print_table
from src.lab04.io_txt_csv import write_csv
from src.lab07.bench import read_numbers
from src.lab07.plot import show_bench_plot
from src.lab10.structures import queue_dequeue, queue_from_list
from src.lab10.linked_list import ll_copy, ll_prepend, ll_from_list


DEFAULT_CSV = "data/lab10/bench.csv"

TIMEOUT = "60"
PRECISION = 4


def list_pop_0(l: list) -> object:
    """ call l.pop(0) """
    return l.pop(0)


def list_insert_0_x(l: list, x) -> None:
    """ call l.insert(0, x)"""
    return l.insert(0, x)


def main():
    """
    Bench stack, queue, linked_list, doubly_linked_list
    """

    parser = argparse.ArgumentParser(description="Benchmark structures")

    parser.add_argument("-t", "--timeout", dest="timeout", type=float, default=TIMEOUT, help="A function tests execution timeout")
    parser.add_argument("-p", "--precision", dest="precision", type=int, default=PRECISION, help="Number of decimal places")
    parser.add_argument("--csv", action="store_true", help="Write results to csv")
    parser.add_argument("--csv-path", dest="csv_str", default=DEFAULT_CSV, help="CSV output path")
    parser.add_argument("--plot", action="store_true", help="Show plot with results")

    args = parser.parse_args()


    # --------------- Data preparation ---------------
    # ! All functions must not make impact on input data
    # Copy data to permit data change.

    numbers_m = read_numbers(Path("data/numbers/values_10_000.csv"))
    numbers_m_queue = queue_from_list(numbers_m)
    numbers_m_ll = ll_from_list(numbers_m)

    numbers_l = read_numbers(Path("data/numbers/values_100_000.csv"))
    numbers_l_queue = queue_from_list(numbers_l)
    numbers_l_ll = ll_from_list(numbers_l)

    num = 42

    # --------------- Declarative tests ---------------

    # Test table line consists of a function, it's complexity and test cases
    # "fn": Callable - the function being tested. Must be pickle-able (anonymous lambda won't work)
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
    queue_tests = [
        {
            "name": "Dequeue (deque.popleft)",
            "complexity": "O(1)",
            "fn": queue_dequeue,
            "cases": [
                {
                    "name": "n=10^4",
                    "args": (deepcopy(numbers_m_queue),),
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "args": (deepcopy(numbers_l_queue),),
                    "number": 5,
                    "repeat": 10,
                }
            ],
        },
        {
            "name": "list.pop(0)",
            "complexity": "O(n)",
            "fn": list_pop_0,
            "cases": [
                {
                    "name": "n=10^4",
                    "args": (deepcopy(numbers_m),),
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "args": (deepcopy(numbers_l),),
                    "number": 5,
                    "repeat": 10,
                }
            ]

        }
    ]

    linked_list_tests = [
        {
            "name": "ll_prepend",
            "complexity": "O(1)",
            "fn": ll_prepend,
            "cases": [
                {
                    "name": "n=10^4",
                    "kwargs": {
                        "head": ll_copy(numbers_m_ll),
                        "value": num,
                    },
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "kwargs": {
                        "head": ll_copy(numbers_l_ll),
                        "value": num,
                    },
                    "number": 5,
                    "repeat": 10,
                },
            ]

        },
        {
            "name": "list.insert(0, x)",
            "complexity": "O(n)",
            "fn": list_insert_0_x,
            "cases": [
                {
                    "name": "n=10^4",
                    "args": (deepcopy(numbers_m), num),
                    "number": 5,
                    "repeat": 10,
                },
                {
                    "name": "n=10^5",
                    "args": (deepcopy(numbers_l), num),
                    "number": 5,
                    "repeat": 10,
                }
            ]

        }
    ]

    tests_table.extend(queue_tests)
    tests_table.extend(linked_list_tests)

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
