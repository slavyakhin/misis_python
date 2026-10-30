import csv
import timeit
import argparse
import multiprocessing as mp
from pathlib import Path
import random
from collections.abc import Sequence
from src.lib.fmt_table import print_table
from src.lab02.arrays import flatten
from src.lab04.io_txt_csv import write_csv
from src.lab07.sorting import bubble_sorted, insertion_sorted, selection_sorted, merge_sorted, counting_sorted
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast


SEED = 42

TIMEOUT = 60 # Maximum execution time (60 seconds in instruction)
PRECISION = 4 # Number of decimal places

REPEAT = 5
NUMBER = 10

REPEAT_S = 5 # 5
NUMBER_S = 10 # 10

REPEAT_M = 1 # 2
NUMBER_M = 2 # 3

REPEAT_L = 1 # 1
NUMBER_L = 1 # 1

LO = -10_000 # numbers_limited lo
HI = 10_000 # numbers_limited hi

REQUEST_COUNT = 10_000 # 10_000


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
    queue: mp.Queue,
    fn,
    args,
    repeat,
    number,
) -> None:
    """
    Subprocess target function.
    Call timeit one single time.
    Put best time in queue.
    """

    times = timeit.repeat(lambda: fn(*args), repeat=repeat, number=number)
    best = min(times) / number
    queue.put(best)


def _timeit_multi_req_worker(
    queue: mp.Queue,
    fn,
    reqs: Sequence[tuple], # Sequence of args
    repeat,
    number,
) -> None:
    """
    Subprocess target function.
    Call timeit len(reqs) times.
    Put total time (around best * len(reqs)) in queue.
    """

    total_time = 0
    for args in reqs:
        times = timeit.repeat(lambda: fn(*args), repeat=repeat, number=number)
        best = min(times) / number
        total_time += best
    queue.put(total_time)


def exec_worker_with_timeout(
    fn_worker,
    fn_args,
    timeout=TIMEOUT,
):
    """
    Exec fn worker, terminate after timeout exceeds.
    Return value from queue
    """

    # Queue will store timeit time values
    # ! One value at a moment !
    queue = mp.Queue()

    process = mp.Process(target=fn_worker, args=(queue, *fn_args))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        raise TimeoutError("The execution exceeded the allowed time limit.")

    return queue.get(timeout=1) if not queue.empty() else None


def _fmt_time(t, timeout, spec=".2f") -> str:
    """
    Format time results
    """
    return format(t, spec) if t is not None else f">{timeout}"


def bench_sorts(timeout=TIMEOUT, precision=PRECISION) -> list:
    """
    Benchmark sort algorithms, print results.
    """

    data_s = read_numbers(Path(f"data/numbers/values_1_000.csv"))
    data_m = read_numbers(Path(f"data/numbers/values_10_000.csv"))
    data_l = read_numbers(Path(f"data/numbers/values_100_000.csv"))

    print("Benchmark sorting")
    rows = [("Algorithm", "Complexity", "n=10^3", "n=10^4", "n=10^5")]

    for name, complexity, fn in [
        ("Timsort", "O(n log n)", sorted),
        ("Merge sort", "O(n log n)", merge_sorted),
        ("Bubble sort", "O(n^2)", bubble_sorted),
        ("Insertion sort", "O(n^2)", insertion_sorted),
        ("Selection sort", "O(n^2)", selection_sorted),
    ]:
        times = []
        for data, repeat, number in [
            (data_s, REPEAT_S, NUMBER_S),
            (data_m, REPEAT_M, NUMBER_M),
            (data_l, REPEAT_L, NUMBER_L),
        ]:
            try:
                t = exec_worker_with_timeout(_timeit_worker, (fn, (data,), repeat, number), timeout=timeout)
            except TimeoutError:
                t = None

            t_str = _fmt_time(t, timeout, spec=f".{precision}f")

            times.append(t_str)

        rows.append((name, complexity, *times))

    # print_table(rows)

    # csv_path = Path("data/lab07/bench_sorts.csv")
    # write_csv(rows, csv_path)

    return rows


def bench_counting_sorted(lo=LO, hi=HI, timeout=TIMEOUT, precision=PRECISION) -> list:
    """
    Benchmark counting sort, print results.
    """

    data_s = read_numbers(Path(f"data/numbers_limited/values_1_000.csv"))
    data_m = read_numbers(Path(f"data/numbers_limited/values_10_000.csv"))
    data_l = read_numbers(Path(f"data/numbers_limited/values_100_000.csv"))

    print("Benchmark counting sort")
    rows = [("Algorithm", "Complexity", "n=10^3", "n=10^4", "n=10^5")]

    name, complexity, fn = "Counting sort", "O(n)", counting_sorted

    times = []
    for data, repeat, number in [
        (data_s, REPEAT_S, NUMBER_S),
        (data_m, REPEAT_M, NUMBER_M),
        (data_l, REPEAT_L, NUMBER_L),
    ]:
        try:
            t = exec_worker_with_timeout(_timeit_worker, (fn, (data, lo, hi), repeat, number), timeout=timeout)
        except TimeoutError:
            t = None

        t_str = _fmt_time(t, timeout, spec=f".{precision}f")

        times.append(t_str)

    rows.append((name, complexity, *times))

    # print_table(rows)

    # csv_path = Path("data/lab07/bench_counting_sorted.csv")
    # write_csv(rows, csv_path)

    return rows


def bench_searches(request_count=REQUEST_COUNT, timeout=TIMEOUT, precision=PRECISION) -> list:
    """
    Benchmark search algorithms, print results
    """

    random.seed(SEED)

    # binary search requires sorted list
    data = sorted(read_numbers(Path(f"data/numbers/values_100_000.csv")))

    # request is args tuple for a search call
    # here data isn't copied, each request has reference to the same data
    requests = [(data, data[random.randint(0, len(data)-1)]) for _ in range(request_count)]

    print(f"Benchmark searches, {request_count=:_}")
    rows = [("Algorithm", "Complexity", "n=10^5")]

    for name, complexity, fn, repeat, number in [
        ("Linear search", "O(n)", linear_search, REPEAT_L, NUMBER_L),
        ("Binary search", "O(log n)", binary_search, REPEAT_S, NUMBER_S),
    ]:
        try:
            t = exec_worker_with_timeout(_timeit_multi_req_worker, (fn, requests, repeat, number), timeout=timeout)
        except TimeoutError:
            t = None
        t_str = _fmt_time(t, timeout, spec=f".{precision}f")

        rows.append((name, complexity, t_str))

    # print_table(rows)

    # csv_path = Path("data/lab07/bench_searches.csv")
    # write_csv(rows, csv_path)

    return rows


def bench_two_sums(timeout=TIMEOUT, precision=PRECISION) -> list:
    """
    Benchmark two sum solutions, print results.
    Return list of dicts - results.
    """

    random.seed(SEED)

    data_s = read_numbers(Path(f"data/numbers/values_1_000.csv"))
    i, j = random.sample(range(len(data_s)), 2)
    target_s = data_s[i] + data_s[j]

    data_m = read_numbers(Path(f"data/numbers/values_10_000.csv"))
    i, j = random.sample(range(len(data_m)), 2)
    target_m = data_m[i] + data_m[j]

    # data_l = read_numbers(Path(f"data/numbers/values_100_000.csv"))
    # i, j = random.sample(range(len(data_l)), 2)
    # target_l = data_l[i] + data_l[j]

    print("Benchmark two sum solutions")
    rows = [("Algorithm", "Complexity", "n=10^3", "n=10^4")]
    # rows = [("Algorithm", "Complexity", "n=10^3", "n=10^4", "n=10^5")]

    for name, complexity, fn, repeat, number in [
        ("Brute", "O(n^2)", two_sum_brute, REPEAT_M, NUMBER_M),
        ("Fast", "O(n)", two_sum_fast, REPEAT_S, NUMBER_S),
    ]:
        times = []
        for data, target in [
            (data_s, target_s),
            (data_m, target_m),
            # (data_l, target_l),
        ]:
            try:
                t = exec_worker_with_timeout(_timeit_worker, (fn, (data, target), repeat, number), timeout=timeout)
            except TimeoutError:
                t = None

            t_str = _fmt_time(t, timeout, spec=f".{precision}f")

            times.append(t_str)

        rows.append((name, complexity, *times))

    # print_table(rows)

    # csv_path = Path("data/lab07/bench_two_sums.csv")
    # write_csv(rows, csv_path)

    return rows


def main():
    """
    Benchmark sort, search and two sum algorithms.
    """
    parser = argparse.ArgumentParser(description="Benchmark algorithms")

    parser.add_argument("-t", "--timeout", dest="timeout", type=float, default=TIMEOUT, help="A function tests execution timeout")
    parser.add_argument("-p", "--precision", dest="precision", type=int, default=PRECISION, help="Number of decimal places")

    args = parser.parse_args()

    rows_sorts = bench_sorts(timeout=args.timeout, precision=args.precision)
    print_table(rows_sorts)
    dicts_sorts = list({rows_sorts[0][i]: value for i, value in enumerate(row)} for row in rows_sorts[1:])

    rows_counting_sorted = bench_counting_sorted(lo=LO, hi=HI, timeout=args.timeout, precision=args.precision)
    print_table(rows_counting_sorted)
    dicts_counting_sorted = list({rows_counting_sorted[0][i]: value for i, value in enumerate(row)} for row in rows_counting_sorted[1:])

    rows_searches = bench_searches(request_count=REQUEST_COUNT, timeout=args.timeout, precision=args.precision)
    print_table(rows_searches)
    dicts_searches= list({rows_searches[0][i]: value for i, value in enumerate(row)} for row in rows_searches[1:])

    rows_two_sums = bench_two_sums(timeout=args.timeout, precision=args.precision)
    print_table(rows_two_sums)
    dicts_two_sums = list({rows_two_sums[0][i]: value for i, value in enumerate(row)} for row in rows_two_sums[1:])

    # Concatenate lists
    dicts = dicts_sorts + dicts_counting_sorted + dicts_searches + dicts_two_sums

    headers = dict.fromkeys(
        flatten(list(
        list(d.keys()) for d in dicts
        )))

    csv_path = Path("data/lab07/bench.csv")
    with csv_path.open("w") as f:
        w = csv.DictWriter(f, headers)
        w.writeheader()
        w.writerows(dicts)


if __name__ == "__main__":
    main()
