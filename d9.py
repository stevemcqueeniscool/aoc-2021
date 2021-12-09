from collections import defaultdict

board = defaultdict(lambda: 10)

for row, ln in enumerate(open("d9.txt").readlines()):
    for col, ch in enumerate(ln.strip()):
        board[(row, col)] = int(ch)


def neighbours(pt):
    x, y = pt
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def is_low(pt):
    return all((board[pt] < board[n] for n in neighbours(pt)))


def explore(pt, basin):
    basin.add(pt)
    for n in neighbours(pt):
        if n not in basin and board[n] >= board[pt] and board[n] < 9:
            explore(n, basin)
    return basin


def solution():
    parta = sum(v + 1 for pt, v in board.copy().items() if is_low(pt))

    basins = [explore(pt, set()) for pt in board.copy() if is_low(pt)]
    basins.sort(key=lambda x: len(x))
    partb = len(basins[-1]) * len(basins[-2]) * len(basins[-3])

    return parta, partb
