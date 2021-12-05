import re
from collections import defaultdict

fname = "d5.txt"


def cmp(a, b):
    return (a > b) - (a < b)


def count_overlap(data):
    board = defaultdict(int)
    for (x0, y0, x1, y1) in data:
        pt = (x0, y0)
        dx = cmp(x1, x0)
        dy = cmp(y1, y0)

        while pt != (x1, y1):
            board[pt] += 1
            pt = (pt[0] + dx, pt[1] + dy)
        board[pt] += 1

    return sum(v > 1 for v in board.values())

 
def d5():
    with open(fname, "r") as f:
        data = [tuple(map(int, re.split(",|->", ln))) for ln in f.readlines()]

    straights = [pt for pt in data if pt[0] == pt[2] or pt[1] == pt[3]]
    return count_overlap(straights), count_overlap(data)
