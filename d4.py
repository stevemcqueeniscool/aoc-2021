from collections import defaultdict

fname = "d4.txt"

def check(idx, data):
    row = (idx // 5) * 5
    col_start = (idx // 25) * 25 + (idx % 5)
    return all(data[i] == 0 for i in range(row, row + 5)) or all(
        data[i] == 0 for i in range(col_start, col_start + 25, 5)
    )


def d4():
    with open(fname, "r") as f:
        xs = map(int, f.readline().rstrip().split(","))
        data = [n for ln in f.readlines() for n in map(int, ln.split())]

    index = defaultdict(set)
    for idx, n in enumerate(data):
        index[n].add(idx)

    for x in xs:
        for idx in index[x]:
            data[idx] = 0
            if check(idx, data):
                board = idx // 25
                return x * sum(data[board * 25 : (board + 1) * 25])
    return None


def d4b():
    with open(fname, "r") as f:
        xs = map(int, f.readline().rstrip().split(","))
        data = [n for ln in f.readlines() for n in map(int, ln.split())]

    index = defaultdict(set)
    for idx, n in enumerate(data):
        index[n].add(idx)

    board_finished = [False] * (len(data) // 25)

    for x in xs:
        for idx in index[x]:
            data[idx] = 0
            board = idx // 25
            if not board_finished[board]:
                board_finished[board] = check(idx, data)
                if all(board_finished):
                    return x * sum(data[board * 25 : (board + 1) * 25])
    return None
