import numpy as np
import itertools
from collections import Counter


directions = [
    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
    ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
    ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), (0, -1, 0), (-1, 0, 0)),
    ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
]


rotations = [np.matrix(d) for d in directions]


def find_shift(pta, ptb):
    for rot in rotations:
        tb = ptb * rot

        aset = set(map(tuple, pta.tolist()))

        for bidx in range(len(ptb)):
            for aidx in range(len(pta)):
                shift = pta[aidx] - tb[bidx]
                shifted = tb + shift
                shifted_set = set(map(tuple, shifted.tolist()))
                if len(shifted_set & aset) >= 12:
                    return shifted_set | aset, shift
    return None, None


def solution():
    xs = [ln.strip() for ln in open("d19.txt").readlines()]
    groups = [
        list(vals) for m, vals in itertools.groupby(xs, lambda ln: ln == "") if not m
    ]

    sensors = []
    for gr in groups:
        pts = [np.matrix(l) for l in gr[1:]]
        all_pts = np.concatenate(pts)
        sensors.append({"name": gr[0], "pts": pts, "all_pts": all_pts})

    points = set(map(tuple, sensors[0]["all_pts"].tolist()))
    centres = {sensors[0]["name"]: np.matrix([0, 0, 0])}

    while len(centres) < len(sensors):
        for sen in sensors:
            if sen["name"] in centres:
                continue

            as_matrix = np.concatenate([np.matrix(d) for d in points])
            check, shift = find_shift(as_matrix, sen["all_pts"])
            if check is not None:
                centres[sen["name"]] = shift
                points = check
                print("sorted : " + sen["name"] + " pts: " + str(len(points)))

    return len(points), max(
        abs(a - b).sum() for a in centres.values() for b in centres.values()
    )
