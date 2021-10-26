from heapq import heappush, heappop, heapify
from collections import deque
from helpers import (
    append_vals, bits_to_str, clear_buf, int_to_bits, read_to_buf
)


class HuffTree:
    def __init__(self, value: int, count: int):
        self.value = value
        self.count = count
        self.left = None
        self.right = None

    def merge(self, other):
        first = HuffTree(self.value, self.count)
        first.left = self.left
        first.right = self.right
        self.value = None
        self.count = first.count + other.count
        self.left = first
        self.right = other

    def __str__(self):
        if self.value is not None:
            return f"{self.count} {self.value}"
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


def counts(in_arr: list[int], n_values: int) -> list:
    """ Takes input array and transforms all the values
        into a dict with different values as keys and
        counts as values. Also transforms the value-count
        pairs into HuffTree nodes.
    """
    d = [0]*(n_values)
    for b in in_arr:
        d[b] += 1

    hufftree_list = []
    for b in range(0, n_values):
        # only add nonzero entries
        if d[b] > 0:
            hufftree_list.append(HuffTree(b, d[b]))

    return hufftree_list


def counts_to_hufftree(count_list: list[HuffTree]) -> HuffTree:
    """ Constructs a Huffman Tree from a list of HuffTree nodes.
    """
    heapify(count_list)
    while len(count_list) > 1:
        node1 = heappop(count_list)
        node2 = heappop(count_list)
        node1.merge(node2)
        heappush(count_list, node1)

    return heappop(count_list)


def hufftree_to_code_lens(code_lens: list, ht: HuffTree,
                          current_len: int) -> list:
    """ Takes a huffman tree and transforms it
        into a list with code lengths corresponding to the length
        of the huffman encoding of the given symbol.
    """
    if ht.value is not None:
        # this does not work correctly when there
        # is a simple node, the max fixes that
        code_lens[ht.value] = max(current_len, 1)
    else:
        hufftree_to_code_lens(code_lens, ht.left, current_len+1)
        hufftree_to_code_lens(code_lens, ht.right, current_len+1)


def canonical_huffcode(bit_lens: list[int]) -> list[list[int]]:
    """ Calculates the canonical huffman code
        from a list of code lengths
    """
    bit_lens_ord = sorted(range(0, len(bit_lens)),
                          key=lambda i: bit_lens[i])
    bit_lens_inv_ord = sorted(range(0, len(bit_lens_ord)),
                              key=lambda i: bit_lens_ord[i])
    bit_lens_sorted = [bit_lens[i] for i in bit_lens_ord]

    # nothing to encode, return empty list
    if bit_lens_sorted[len(bit_lens_sorted)-1] == 0:
        return [[]]*len(bit_lens)

    i = 0
    output = []
    while bit_lens_sorted[i] == 0:
        output.append([])
        i += 1
    output.append([0]*bit_lens_sorted[i])
    code = 0
    i += 1
    while i < len(bit_lens_sorted):
        code = code + 1 << bit_lens_sorted[i] - bit_lens_sorted[i-1]
        output.append(list(reversed(int_to_bits(code, bit_lens_sorted[i]))))
        i += 1

    return [output[i] for i in bit_lens_inv_ord]


def get_codes(vals: list[int], n_vals: int) -> (list[int], list[list[int]]):
    """ Gets list of values and returns their code lengths
        and the respective codes.
    """
    counts_dict = counts(vals, n_vals)
    hufftree = counts_to_hufftree(counts_dict)
    code_lens = [0]*n_vals
    hufftree_to_code_lens(code_lens, hufftree, 0)
    return (code_lens, canonical_huffcode(code_lens))


def rle(bit_lengths: list[int]) -> bytearray:
    """ RLE implementation

        Assumes that the elements of 'bit_lengths'
        are integers between 0 and 255.
    """
    current = bit_lengths[0]
    current_count = 1
    output = bytearray()
    for i in range(1, len(bit_lengths)):

        # next byte matches current byte
        if current_count < 255 and bit_lengths[i] == current:
            current_count += 1
        # next byte differs, append current byte along with its count to output
        # and set new current byte and current count
        else:
            output += current_count.to_bytes(1, 'big')
            output += current.to_bytes(1, 'big')
            current = bit_lengths[i]
            current_count = 1

    # append last byte along with its count
    output += current_count.to_bytes(1, 'big')
    output += current.to_bytes(1, 'big')

    return output


def huff_encode(in_arr: bytearray) -> bytearray:
    """ Encodes the input array using Canonical Huffman Encoding.
    """
    in_vals = deque(in_arr)
    in_vals.append(256)
    (code_lens, codes) = get_codes(list(in_vals), 257)

    out = bytearray()

    # add rle bitlengths
    out += rle(code_lens)

    # add input data
    out_buf = deque([])
    while len(in_vals) > 0:
        val = in_vals.popleft()
        append_vals(out_buf, codes[val])
        clear_buf(out, out_buf, 7)

    # add rest of the buffer
    clear_buf(out, out_buf, 0)

    return out


def read_code_dict(in_vals: deque[int], n_vals: int) -> dict[str, int]:
    """ Reads code dict from input values, assuming its encoded using
        Canonical Huffman Coding and RLE for the code lengths.
        Returns the dict.
    """
    bit_lengths = []
    while len(bit_lengths) < n_vals:
        count = in_vals.popleft()
        val = in_vals.popleft()
        for j in range(0, count):
            bit_lengths.append(val)
    keys = canonical_huffcode(bit_lengths)
    codes = {}
    for j in range(0, n_vals):
        if len(keys[j]) > 0:
            codes[bits_to_str(keys[j])] = j

    return codes


def read_code(in_vals: deque[int], in_buf: deque[str],
              codes: dict[str, int]) -> int:
    """ Reads characters from the input value until it finds
        a code thats included in the codes dictionary.
        Returns the value of the code.
    """

    key = ""
    while key not in codes:
        read_to_buf(in_vals, in_buf, 1)
        key += in_buf.popleft()
    return codes[key]


def huff_decode(in_arr: bytearray) -> bytearray:
    """ Decodes the input array assuming it was encoded with
        Canonical Huffman Encoding
    """
    in_vals = deque(in_arr)
    codes = read_code_dict(in_vals, 257)

    out = bytearray()
    in_buf = deque([])
    code = read_code(in_vals, in_buf, codes)
    while code != 256:
        out += code.to_bytes(1, 'big')
        code = read_code(in_vals, in_buf, codes)

    return out