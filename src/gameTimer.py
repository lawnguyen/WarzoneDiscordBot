import time

__all__ = ["start_timer", "get_time_elapsed"]

_start_time = None

def start_timer():
    _start_time = time.time()

def get_time_elapsed():
    time_now = time.time()
    return time_now - _start_time