import time
import threading
import os

indicator = ("—", "\\", "|", "/")
# indicator = ("⠋⠁ ", "⠉⠉ ", "⠈⠉⠁", " ⠉⠉", " ⠈⠙", "  ⠹", "  ⠼", " ⠠⠴", " ⠤⠤", "⠠⠤⠄", "⠤⠤ ", "⠦⠄ ", "⠧  ", "⠏  ")
# indicator = ("⠋⠁", "⠉⠉", "⠈⠙", " ⠹", " ⠼", "⠠⠴", "⠤⠤", "⠦⠄", "⠧ ", "⠏ ")

def stopwatch_worker(stop_event: threading.Event):
    start = time.perf_counter()
    i = 0
    while not stop_event.is_set():
        print(f"_{time.perf_counter()-start:.2f}s {indicator[i]} elapsed\r", end="")
        i = (i + 1) % (len(indicator))
        time.sleep(0.2)
