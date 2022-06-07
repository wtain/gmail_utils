from functools import partial


class LogCall:

    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __call__(self, obj, *args, **kwargs):
        print("Calling " + self.function.__name__)
        print("Parameters: " + str(*args))
        result = self.function(obj, *args, **kwargs)
        if type(result) is list:
            print("Returning list len=" + len(result))
        else:
            print("Returning " + result)
        return result
