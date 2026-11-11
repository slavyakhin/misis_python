import timeit
import logging
import multiprocessing as mp
from pathlib import Path
from multiprocessing.connection import Connection 
from collections.abc import Sequence, Callable


TIMEOUT = 60 # Maximum execution time (60 seconds in instruction)

REPEAT = 1
NUMBER = 1

LOG_DIR = "logs"


def setup_worker_logger(log_dir: str | Path = Path(LOG_DIR)) -> logging.Logger:
    """ Configure logger for subprocess """

    log_dir = Path(log_dir)

    # ensure directory
    log_dir.mkdir(parents=True, exist_ok=True)

    process = mp.current_process()
    log_file = log_dir / f"worker_{process.pid}.log"

    logger = mp.get_logger()
    logger.setLevel(level=logging.DEBUG)

    handler = logging.FileHandler(log_file, mode="a")
    handler.setLevel(level=logging.DEBUG)

    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


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

    logger = setup_worker_logger()
    logger.info("Worker started")

    try:
        with writer_conn: # Close connection automatically
            total_time = 0
            for args, kwargs in reqs:
                try:
                    times = timeit.repeat(lambda: fn(*args, **kwargs), number=number, repeat=repeat)
                except:
                    logger.exception("timeit failed")
                    raise
                best = min(times) / number
                total_time += best
            
            logger.info("Worker successfully done")
            writer_conn.send(total_time)

    except:
        # logger.debug("Worker failed!") // Works
        # logger.exception("Worker failed") // PUZZLE! Why not working?
        raise

    finally:

        for handler in logger.handlers[:]:
            handler.flush()
            handler.close()
            logger.removeHandler(handler)


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
    return format(t, spec) if t is not None else f">{timeout:{spec}}"


def start_benchmark(tests_table: list[dict], timeout: float | int, precision: int) -> list[dict]:
    """
    Benchmark given strict formatted tests_table (see comments or README).

    Returns result recs list.
    
    Prints logs.
    """

    # --------------- Declarative tests ---------------

    # Test table line consists of a function, it's complexity and test cases
    # "fn": Callable - the function being tested. Must be pickle-able
    # "complexity": str

    # Test case is a dictionary with required keys:
    # "name": str - name of case (e.g. "n=10^3")
    # ----- bench args -----
    # PICKE - all objects must be picke-able (see __reduce__ method)
    #
    # "reqs": list[tuple[tuple, dict]] - list of (args, kwargs) requests
    # If "reqs" is missing -> use args, kwargs as the only one request
    # "args": tuple - the function's args
    # "kwargs": dict - the function's kwargs

    # "number": int - timeit number
    # "repeat": int - timeit repeat
    # "timeout": float | int

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
                timeout=case.get("timeout", timeout),
            )

            t_str = _fmt_time(t, timeout, spec=f".{precision}f")
            result_recs[i][case["name"]] = t_str

    return result_recs
