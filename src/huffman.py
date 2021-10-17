from heapq import heappush, heappop, heapify
from helpers import bits_to_byte, int_to_bit_str, rle


class HuffTree:
    def __init__(self, byte: bytes, count: int):
        self.byte = byte
        self.count = count
        self.left = None
        self.right = None

    def merge(self, other):
        first = HuffTree(self.byte, self.count)
        first.left = self.left
        first.right = self.right
        self.byte = None
        self.count = first.count + other.count
        self.left = first
        self.right = other

    def __str__(self):
        if self.byte is not None:
            return f"{self.count} {self.byte}"
        else:
            return str(self.count) + ": ( " + \
                    self.left.__str__() + ", " + self.right.__str__() + \
                    " )"

    # for printing with heapq
    def __repr__(self):
        return self.__str__()

    # for this to work with heapq
    def __lt__(self, other):
        return self.count < other.count


def byte_counts(input_bytes: bytearray) -> list:
    d = [0]*257
    for b in input_bytes:
        d[b] += 1

    hufftree_list = []
    for b in range(0, 257):
        hufftree_list.append(HuffTree(b, d[b]))

    return hufftree_list


def counts_to_hufftree(count_list: list) -> HuffTree:
    heapify(count_list)
    while len(count_list) > 1:
        node1 = heappop(count_list)
        node2 = heappop(count_list)
        node1.merge(node2)
        heappush(count_list, node1)

    return heappop(count_list)


def hufftree_to_keys(ht: HuffTree, key: int,
                     lst: list) -> list:
    if ht.byte is not None:
        lst[ht.byte] = key
        return lst
    else:
        lst = hufftree_to_keys(ht.left, key+[0], lst)
        lst = hufftree_to_keys(ht.right, key+[1], lst)
        return lst


def huff_encode(input_bytes: bytearray) -> bytearray:

    counts_dict = byte_counts(input_bytes)
    hufftree = counts_to_hufftree(counts_dict)
    keys_empty = [[]]*257
    keys = hufftree_to_keys(hufftree, [], keys_empty)

    output = bytearray()

    # add rle bitlengths
    output += rle(list(map(len, keys)))

    # add codes
    output_buffer = []
    for i in range(0, 257):
        output_buffer += keys[i]
        while len(output_buffer) >= 8:
            output += bits_to_byte(output_buffer[:8])
            output_buffer = output_buffer[8:]

    # add input data
    for byte in input_bytes:
        output_buffer += keys[byte]
        while len(output_buffer) >= 8:
            output += bits_to_byte(output_buffer[:8])
            output_buffer = output_buffer[8:]

    output_buffer += keys[256]
    # add rest of the buffer
    while len(output_buffer) > 0:
        output += bits_to_byte(output_buffer[:8])
        output_buffer = output_buffer[8:]

    return output


def huff_decode(input_bytes: bytearray) -> bytearray:
    bit_lengths = []

    i = 0
    while len(bit_lengths) < 257:
        count = input_bytes[i]
        val = input_bytes[i+1]
        for j in range(0, count):
            bit_lengths.append(val)
        i += 2

    codes = {}
    input_buffer = ""
    for j in range(0, 257):
        while len(input_buffer) < bit_lengths[j]:
            input_buffer += int_to_bit_str(input_bytes[i])
            i += 1
        codes[input_buffer[:bit_lengths[j]]] = j
        input_buffer = input_buffer[bit_lengths[j]:]

    output = bytearray()
    current_char = ""
    while True:
        while current_char not in codes:
            if len(input_buffer) == 0:
                input_buffer += int_to_bit_str(input_bytes[i])
                i += 1
            current_char += input_buffer[0]
            input_buffer = input_buffer[1:]
        if codes[current_char] == 256:
            break
        else:
            output += codes[current_char].to_bytes(1, 'big')
            current_char = ''

    return output
