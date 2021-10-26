from math import floor, log
from collections import deque


def bits_to_str(lst: list[int]) -> str:
    """ Transforms a list of bits into a string of bits.
    """
    output = ""
    for i in lst:
        output += str(i)
    return output


def bits_to_int(bits: list[int]) -> int:
    """ Transforms a list of bits into an integer
    """
    output = 0
    for i in range(0, len(bits)):
        output += 2**i * bits[i]
    return output


def bits_to_byte(bits: list[int]) -> bytes:
    """ Tranforms list of bits to a byte type
        only works for length <= 8.
    """
    return bits_to_int(bits).to_bytes(1, 'big')


def int_to_bits(b: int, out_len: int = 8) -> list[int]:
    """ Transforms an integer to a list of bits of length out_len.
    """
    output = []
    for i in range(0, out_len):
        output.append(b % 2)
        b = b // 2

    return output


def int_to_bitlen(b: int) -> int:
    """ Calculates the number of bits required to represent
        the given integer.
    """
    return floor(log(b, 2)+1)


def int_to_min_bits(b: int) -> list[int]:
    """ Transforms an integer into a list of bits
        where the list length is as short as possible.
    """
    return int_to_bits(b, int_to_bitlen(b))


def int_to_bit_str(b: int) -> str:
    """ Transforms the integer into a string of bits
        representing the integer.
    """
    return bits_to_str(int_to_bits(b))


def clear_buf(out: bytearray(), out_buf: deque[int], until_len: int = 7):
    """ Removes extra bits from out_buf until
        size of the buffer is until_len
    """
    while len(out_buf) > until_len:
        bitlist = []
        for i in range(0, min(len(out_buf), 8)):
            bitlist.append(out_buf.popleft())
        out.append(bits_to_int(bitlist))


def append_vals(buf: deque, lst: list):
    """ Takes values from a list and appends then into a deque
    """
    for x in lst:
        buf.append(x)


def read_to_buf(in_vals: deque[int], in_buf: deque[str], min_len: int):
    """ Reads input values until in_buf has at least min_len bits of data
    """
    while len(in_buf) < min_len:
        append_vals(in_buf, int_to_bit_str(in_vals.popleft()))
