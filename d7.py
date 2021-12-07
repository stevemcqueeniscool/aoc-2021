import statistics
import math


xs = eval(f'[{open("d7.txt").readline()}]')


def weight(x):
    return (x * (x + 1)) // 2


def solution_brute_force():
    parta = min(sum(abs(x - y) for x in xs) for y in xs)

    start, end = min(xs), max(xs)
    partb = min(sum(weight(abs(x - y)) for x in xs) for y in range(start, end + 1))

    return parta, partb


def solutionb():
    med = int(statistics.median(xs))
    parta = sum(abs(x - med) for x in xs)

    mean = statistics.mean(xs)
    ys = int(math.floor(mean)), int(math.ceil(mean))
    partb = min(sum(weight(abs(x - y)) for x in xs) for y in ys)

    return parta, partb
