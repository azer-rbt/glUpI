import time

class DelayedTask:
    def __init__(self, func, delay):
        self.func = func
        self.delay = delay
        self.sub = 0
    def check(self, elapsed):
        if self.sub == 0:
            self.sub = elapsed
        if elapsed - self.sub > self.delay:
            self.func()
            return False
        return True

class RepeatedTask:
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval
        self.sub = 0
    def check(self, elapsed):
        if self.sub == 0:
            self.sub = elapsed
        if elapsed - self.sub > self.interval:
            self.sub = elapsed
            res = self.func()
            return res
        return True

class Time:
    def __init__(self):
        self.start = time.perf_counter()
        self.fps = 30
        self.delta_time = 0
        self.tasks = []
    def set_fps(self, fps):
        self.fps = fps
    def set_delta_time(self, dt):
        self.delta_time = dt
    def get_elapsed(self):
        return time.perf_counter() - self.start

    def check_tasks(self):
        stopped_tasks: [int] = []
        for i in range(len(self.tasks)):
            res = self.tasks[i].check(self.get_elapsed())
            if res is False:
                stopped_tasks.append(i)
        for i in stopped_tasks:
            self.tasks.pop(i)
    def add_delayed_task(self, delay, func):
        self.tasks.append(DelayedTask(func, delay))
    def add_repeated_task(self, interval, func):
        self.tasks.append(RepeatedTask(func, interval))
