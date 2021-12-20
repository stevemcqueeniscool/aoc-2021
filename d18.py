import copy
from functools import reduce

exprs = [eval(l) for l in open("d18.txt").readlines()]


def lookup(xs, path):
    r = xs
    for p in path:
        r = r[p]
    return r


def path_set(xs, path, value):
    xs_copy = xs  # copy.deepcopy(xs)
    r = xs_copy
    for p in path[:-1]:
        r = r[p]
    r[path[-1]] = value
    return xs_copy


def find_exploder(xs):
    st = [[]]
    explode_path = None
    last_value_path = None
    next_value_path = None

    while st:
        path = st.pop()

        node = lookup(xs, path)
        if type(node) == list and len(path) == 4 and explode_path is None:
            explode_path = path
            continue

        if type(node) == list:
            st.append(path + [1])
            st.append(path + [0])
        else:
            if explode_path is None:
                last_value_path = path
            else:
                next_value_path = path
                break

    return explode_path, last_value_path, next_value_path


def do_explode(xs, path, last_path, next_path):
    a, b = lookup(xs, path)
    r = path_set(xs, path, 0)
    if last_path:
        r = path_set(r, last_path, lookup(r, last_path) + a)
    if next_path:
        r = path_set(r, next_path, lookup(r, next_path) + b)
    return r


def find_split(xs):
    st = [[]]
    while st:
        path = st.pop()
        node = lookup(xs, path)
        if type(node) == list:
            st.append(path + [1])
            st.append(path + [0])
        elif node > 9:
            return path
    return None


def do_split(xs, path):
    val = lookup(xs, path)
    a = val // 2
    b = val - a
    return path_set(xs, path, [a, b])


def adder(xsa, xsb):
    xs = [copy.deepcopy(xsa), copy.deepcopy(xsb)]
    while True:
        path, lastp, nextp = find_exploder(xs)
        if path:
            xs = do_explode(xs, path, lastp, nextp)
            continue

        path = find_split(xs)
        if path:
            xs = do_split(xs, path)
            continue
        break
    return xs


def magnitude(xs):
    return xs if type(xs) == int else 3 * magnitude(xs[0]) + 2 * magnitude(xs[1])


def parta():
    return magnitude(reduce(adder, exprs))


def partb():
    return max(
        magnitude(adder(exprs[i], exprs[j]))
        for i in range(len(exprs))
        for j in range(len(exprs))
        if j != i
    )
