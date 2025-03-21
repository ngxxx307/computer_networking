# https://scis.uohyd.ac.in/~atulcs/computernetworks/lab5.html
from dataclasses import dataclass, field
from typing import Callable

import random

packet_size = 20
corruption_prob: float = 0.2
loss_prob: float = 0.1


@dataclass
class Packet:
    seqnum: int = 0
    acknum: int = 0
    checksum: int = 0
    payload: bytes = b""


@dataclass
class msg:
    data: str


def bytes_sum(b: bytes) -> int:
    # Loop over the bytes in steps of 2
    Sum = 0
    for i in range(0, len(b), 2):
        chunk = b[i : i + 2]
        value = int.from_bytes(chunk, byteorder="big")
        Sum += value
    return Sum % 65536


def checksum(b: bytes, Sum: int):
    return (bytes_sum(b) + Sum) == 65535


def randomly_corrupt(b: bytes) -> bytes:
    b_arr = bytearray(b)
    total_bits = len(b_arr) * 8

    bit_to_flip = random.randint(0, total_bits)
    byte_index = (bit_to_flip // 8) - 1
    bit_pos = bit_to_flip % 8
    b_arr[byte_index] ^= 1 << bit_pos

    return bytes(b_arr)


class Host:
    def __init__(self, to_layer3: Callable[[Packet, int], None]):
        self.to_layer3 = to_layer3
        return

    def input(self, pkt: Packet):  # Called when packet is received from layer 3
        print(f"Received: {pkt.payload}")

        if not checksum(pkt.payload, pkt.checksum):
            print("Checksum failed")
        return

    def output(self, msg: str, host_num: int):  # Called by layer 5
        encoded_msg = msg.encode("utf-8")

        base = 0

        while base < len(encoded_msg):
            t = encoded_msg[base : base + packet_size]

            pkt = Packet(payload=t, checksum=bytes_sum(t) ^ 0xFFFF)
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
        if random.random() < loss_prob:  # Simulate packet loss
            return
        if random.random() < corruption_prob:  # Simulate packet corruption
            pkt.payload = randomly_corrupt(pkt.payload)
        if h:
            h.input(pkt)


def main():
    s = simulator()

    host1 = Host(s.layer3_send)
    host2 = Host(s.layer3_send)

    s.register(host1, 1)
    s.register(host2, 2)

    with open(
        "/Users/kurtng/Documents/computer_networking/chapter_03/alice.txt", "r"
    ) as file:
        message = file.read()
        host1.output(message, 2)
    return


main()
