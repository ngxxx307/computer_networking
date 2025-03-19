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


class Host:
    def input(self, pkt: Packet):  # Called when packet is received from layer 3
        return

    def output(self, msg: str, host_num: int):  # Called by layer 5
        return

    def to_layer3(
        self, pkt: Packet, host_num: int
    ):  # Called when packet is received from layer 3
        return


class sender(Host):
    def __init__(self):
        return

    def output(self, msg: str, host_num: int):  # Called by layer 5
        return

    def to_layer3(
        self, pkt: Packet, host_num: int
    ):  # Called when packet is received from layer 3
        return


class receiver(Host):
    def __init__(self):
        return


class simulator:
    hosts: list[Host | None] = []

    def __init__(self):
        return

    def register(self, host: Host, num: int):
        if num < len(self.hosts):
            self.hosts[num] = host
        else:
            while len(self.hosts) < num:
                self.hosts.append(None)
            self.hosts.append(host)

    def layer3_send(self, host_num: int, pkt: Packet):
        h = self.hosts[host_num]
        if h:
            h.input(pkt)


def main():
    s = simulator()
    return
