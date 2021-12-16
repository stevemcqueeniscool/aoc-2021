import operator
import functools


hs = open("d16.txt").read().strip()


class Bits:
    def __init__(self, hs):
        self._bs = "".join(format(int(f"0x{h}", 16), "04b") for h in hs)
        self._ptr = 0

    def pop(self, bits):
        q = self._bs[self._ptr : self._ptr + bits]
        self._ptr += bits
        return int(q, 2)


def read_literal(b, version):
    val, more = 0, 1
    while more:
        more = b.pop(1)
        val = (val << 4) + b.pop(4)
    return {"type": "literal", "version": version, "value": val}


def read_operator(b, version, type_id):
    if b.pop(1) == 1:
        num_sub_packets = b.pop(11)
        values = [read_packet(b) for _ in range(num_sub_packets)]
    else:
        num_bits = b.pop(15)
        target = b._ptr + num_bits
        values = []
        while b._ptr != target:
            values.append(read_packet(b))
    return {
        "type": "operator",
        "version": version,
        "type_id": type_id,
        "values": values,
    }


def read_packet(b):
    version = b.pop(3)
    type_id = b.pop(3)
    if type_id == 4:
        return read_literal(b, version)
    else:
        return read_operator(b, version, type_id)


def count_versions(packet):
    result = packet["version"]
    if packet["type"] == "operator":
        result += sum(count_versions(sp) for sp in packet["values"])
    return result


def evaluate(packet):
    if packet["type"] == "literal":
        return packet["value"]
    else:
        type_id = packet["type_id"]
        args = [evaluate(p) for p in packet["values"]]
        if type_id == 0:
            return sum(args)
        elif type_id == 1:
            return functools.reduce(operator.mul, args, 1)
        elif type_id == 2:
            return min(args)
        elif type_id == 3:
            return max(args)
        elif type_id == 5:
            return int(args[0] > args[1])
        elif type_id == 6:
            return int(args[0] < args[1])
        elif type_id == 7:
            return int(args[0] == args[1])
    return None


def solution(hs):
    packets = read_packet(Bits(hs))
    return count_versions(packets), evaluate(packets)
