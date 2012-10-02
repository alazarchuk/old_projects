try:
    import psyco
    psyco.full()
except ImportError:
    print 'Psyco not installed, the program will just run slower'

import time

from threading import Thread

CNT = 40000000

def count(n):
    sum(xrange(n))


def time_it(func):
    strt = time.time()
    func()
    print (func.__name__, time.time() - strt)

def seq():
    count(CNT)
    count(CNT)
    count(CNT)

def parll():
    t1 = Thread(target=count, args=(CNT, ))
    t2 = Thread(target=count, args=(CNT, ))
    t3 = Thread(target=count, args=(CNT, ))
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


if __name__ == '__main__':
    time_it(seq)
    time_it(parll)
