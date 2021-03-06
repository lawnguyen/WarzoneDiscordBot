import time

class Timer():
    def __init__(self):
        self._start_time = None

    def restart_timer(self):
        self._start_time = time.time()

    def get_time_elapsed(self):
        if (self._start_time == None):
            return 0
        time_now = time.time()
        return time_now - self._start_time