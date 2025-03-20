# https://scis.uohyd.ac.in/~atulcs/computernetworks/lab5.html
from dataclasses import dataclass, field
from typing import Callable

packet_size = 20


@dataclass
class Packet:
    seqnum: int = 0
    acknum: int = 0
    checksum: int = 0
    payload: bytes = b""


@dataclass
class msg:
    data: str


class Host:
    def __init__(self, to_layer3: Callable[[Packet, int], None]):
        self.to_layer3 = to_layer3
        return

    def input(self, pkt: Packet):  # Called when packet is received from layer 3
        print(f"Received: {pkt.payload}")
        return

    def output(self, msg: str, host_num: int):  # Called by layer 5
        encoded_msg = msg.encode("utf-8")

        base = 0

        while base < len(encoded_msg):
            pkt = Packet(payload=encoded_msg[base : base + packet_size])
            self.to_layer3(pkt, host_num)
            base += packet_size


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

    def layer3_send(self, pkt: Packet, host_num: int):
        h = self.hosts[host_num]
        if h:
            h.input(pkt)


def main():
    s = simulator()

    host1 = Host(s.layer3_send)
    host2 = Host(s.layer3_send)

    s.register(host1, 1)
    s.register(host2, 2)

    with open("alice.txt", "r") as file:
        message = file.read()
        host1.output(message, 2)
    return


main()
