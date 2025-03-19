# https://scis.uohyd.ac.in/~atulcs/computernetworks/lab5.html
from dataclasses import dataclass, field


@dataclass
class Packet:
    seqnum: int = 0
    acknum: int = 0
    checksum: int = 0
    payload: str = field(default_factory=lambda: " " * 20)


@dataclass
class msg:
    data: str = field(default_factory=lambda: " " * 20)


class sender:
    def __init__(self):
        return

    def output(sel, msg: str):  # Called by layer 5
        return

    def input(self, pkt: Packet):  # Called when packet is received from layer 3
        return


class receiver:
    def __init__(self):
        return

    def input(self, pkt: Packet):  # Called when packet is received from layer 3
        return


def main():
    return
