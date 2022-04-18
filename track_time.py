import timeit
from functools import partial


class track_time:

    def __init__(self, function, min_duration=1):
        self.function = function
        self.min_duration = min_duration

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __call__(self, obj, *args, **kwargs):
        start = timeit.default_timer()
        result = self.function(obj, *args, **kwargs)
        stop = timeit.default_timer()
        duration = stop - start
        if duration > self.min_duration:
            print(self.function.__name__ + " took " + "{:.6f}".format(duration))
        return result
