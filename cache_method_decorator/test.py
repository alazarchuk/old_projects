import time


def cachedmethod(function):
    return Memoize(function)


class Memoize(object):
    def __init__(self, fn):
        self.cache = {}
        self.fn = fn

    def __get__(self, instance, cls=None):
        self.instance = instance
        return self

    def __call__(self, *args, **kwds):
        key = kwds and (args, frozenset(kwds.iteritems())) or args
        if self.cache.has_key(key):
            return self.cache[key]
        else:
            object = self.cache[key] = self.fn(self.instance, *args, **kwds)
            return object


if __name__ == '__main__':
    from math import sqrt,log,sin,cos

    class Example:
        def __init__(self,x,y):
            # self._x and self._y should not be changed after initialization
            self._x = x
            self._y = y

        @cachedmethod
        def computeSomething(self, alpha, beta):
            time.sleep(1)
            w = log(alpha) * sqrt(self._x * alpha + self._y * beta)
            z = log(beta) * sqrt(self._x * beta + self._y * alpha)
            return sin(z) / cos(w)

    ex = Example(1, 2)
    print ex.computeSomething(0.1, 0.2)
    print ex.computeSomething(0.1, 0.2)
