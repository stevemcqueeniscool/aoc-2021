board = set()
_lns = [ln.strip() for ln in open("d20.txt").readlines()]
key = set(idx for idx, ch in enumerate(_lns[0]) if ch == "#")
for row, ln in enumerate(_lns[2:]):
    for col, ch in enumerate(ln.strip()):
        if ch == "#":
            board.add((col, row))


def find_bounds(board):
    minx = min(x for x, y in board)
    miny = min(y for x, y in board)
    maxx = max(x for x, y in board)
    maxy = max(y for x, y in board)
    return minx, miny, maxx, maxy


pow2 = [2 ** x for x in reversed(range(9))]


def getval(board, value, x, y):
    vs = [
        value if (x + dx, y + dy) in board else int(not bool(value))
        for dy in [-1, 0, 1]
        for dx in [-1, 0, 1]
    ]
    return sum(a * b for (a, b) in zip(vs, pow2))


def iterate2(key, board):
    minx, miny, maxx, maxy = find_bounds(board)

    b1 = set()
    for y in range(miny - 2, maxy + 2 + 1):
        for x in range(minx - 2, maxx + 2 + 1):
            v = getval(board, 1, x, y)
            if v not in key:
                b1.add((x, y))  # store zeros

    minx, miny, maxx, maxy = find_bounds(b1)

    b2 = set()
    for y in range(miny - 2, maxy + 2 + 1):
        for x in range(minx - 2, maxx + 2 + 1):
            v = getval(b1, 0, x, y)
            if v in key:
                b2.add((x, y))  # store ones

    return b2


def solution():
    b = iterate2(key, board)
    parta = len(b)
    for _ in range(24):
        b = iterate2(key, b)
    return parta, len(b)
