from functools import cache
from collections import Counter

lns = open("d14.txt").readlines()
starting_str = lns[0].strip()
rules = {ln[:2]: ln[6] for ln in lns[2:]}


@cache
def calc_hist(pair, steps):
    if steps == 0:
        return Counter(pair)
    inserted = rules[pair]
    left, right = pair[0] + inserted, inserted + pair[1]
    result = calc_hist(left, steps - 1) + calc_hist(right, steps - 1)
    result[inserted] -= 1
    return result


def solution(steps):
    result = Counter(starting_str[0])
    for ch1, ch2 in zip(starting_str, starting_str[1:]):
        result += calc_hist(ch1 + ch2, steps)
        result[ch1] -= 1
    return max(result.values()) - min(result.values())


parta = solution(10)
partb = solution(40)
