import itertools

inputs = [
    [e.strip().split() for e in ln.split("|")] for ln in open("d8.txt").readlines()
]

sorry = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6}

baseline = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def find_perm(codes, current):
    input_s = set(frozenset(chs) for chs in codes)

    for perm in itertools.permutations("abcdefg"):
        mapper = {
            frozenset(perm[sorry[ch]] for ch in baseline[digit]): digit
            for digit in range(10)
        }

        if mapper.keys() == input_s:
            return (
                1000 * mapper[frozenset(current[0])]
                + 100 * mapper[frozenset(current[1])]
                + 10 * mapper[frozenset(current[2])]
                + mapper[frozenset(current[3])]
            )

    return None


def solution():
    target = set((2, 3, 4, 7))
    parta = sum(1 for ln in inputs for word in ln[1] if len(word) in target)
    partb = sum(find_perm(ln[0], ln[1]) for ln in inputs)
    return parta, partb
