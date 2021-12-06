import functools


@functools.cache
def rec_count(x, days):
    return 1 + sum(rec_count(8, i) for i in range(days - x - 1, -1, -7))


def solution():
    xs = eval(f'[{open("d6.txt").readline()}]')
    soln = lambda days: sum(rec_count(x, days) for x in xs)
    return soln(80), soln(256)
