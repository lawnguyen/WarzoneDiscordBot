import time

class Timer():
    def __init__(self):
        self._start_time = None

    def start_timer(self):
        self._start_time = time.time()

    def get_time_elapsed(self):
        time_now = time.time()
        return time_now - self._start_time