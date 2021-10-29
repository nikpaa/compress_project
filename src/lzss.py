from collections import deque
from helpers import int_to_bitlen


class LZSSNode:
    def __init__(self, char: int = None,
                 dist: int = None, length: int = None):
        if char is None and (dist is None or length is None):
            e = 'Either "char" or "dist" and "length" have to be defined'
            raise Exception(e)
        elif char is None:
            self.dist = dist
            self.length = length
            self.type = 'match'
        else:
            self.char = char
            self.type = 'literal'

    def __str__(self) -> str:
        if self.type == 'literal':
            return f'\'{chr(self.char)}\''
        else:
            return f'<{self.dist},{self.length}>'

    def value(self) -> (int, int):
        if self.type == 'literal':
            return (self.char, None)
        else:
            return (self.dist, self.length)

    def is_literal(self) -> bool:
        return self.type == 'literal'

    def defl_sym(self) -> int:
        if self.is_literal():
            return self.char
        else:
            return int_to_bitlen(self.length) + 255

    def defl_dist(self) -> int:
        if self.is_literal():
            return None
        else:
            return int_to_bitlen(self.dist)

    # for printing (debugging)
    def __repr__(self):
        return self.__str__()


def append_chars(out: deque[LZSSNode], char_buf: deque[int]):
    """ Transforms characters in char_buf to LZSS nodes
        and appends them to out.
    """
    while len(char_buf) > 0:
        out.append(LZSSNode(char=char_buf.popleft()))


def append_ref(out: deque[LZSSNode], length: int, dist: int):
    """ Takes length and distance of reference
        and appends it to out.
    """
    out.append(LZSSNode(dist=dist, length=length))


def append_lzss_node(out: deque[LZSSNode], pos: int,
                     char_buf: deque[int], in_buf: list[int]):
    """ Makes sure that only matches with 3 or longer len
        are appended as reference.
        Otherwise it is appended as a literal character.
    """
    if len(char_buf) >= 3:
        append_ref(out, len(char_buf), len(in_buf)-pos-len(char_buf))
        char_buf.clear()
    else:
        append_chars(out, char_buf)


def buffer_find_from(pos: int, char_buf: deque[int], in_buf: list[int]) -> bool:
    """ Checks if 'char_buf' is in 'in_buf' starting from 'pos'
    """
    for i in range(0, len(char_buf)):
        if char_buf[i] != in_buf[pos+i]:
            return False
    return True


def buffer_find(char_buf: deque[int], in_buf: list[int],
                starting_pos: int = -1) -> int:
    """ Checks if 'char_buf' is included in 'in_buf'
        Returns 'pos' of matched string if found,
        otherwise returns -1
    """
    pos = starting_pos if starting_pos >= 0 else len(in_buf) - len(char_buf)
    while pos >= 0:
        if buffer_find_from(pos, char_buf, in_buf):
            return pos
        pos -= 1
    return pos


def handle_new_character(c: int, pos: int, in_buf: list[int],
                         char_buf: deque[int], out: deque[LZSSNode]) -> int:
    """ Handles a new character:
        if there is a previous match, checks if the match can be elongated;
        if not, checks if the new character can be matched separately.
        Returns updated pos of a match.
    """
    if pos >= 0:
        char_buf.append(c)
        new_pos = buffer_find(char_buf, in_buf, pos)
        if new_pos >= 0:
            return new_pos
        else:
            char_buf.pop()
            append_lzss_node(out, pos, char_buf, in_buf)
            char_buf.clear()

    char_buf.append(c)
    pos = buffer_find(char_buf, in_buf)
    if pos >= 0:
        return pos
    else:
        append_chars(out, char_buf)
        return pos


def to_lzss(in_arr: bytearray, buffer_size: int) -> deque[LZSSNode]:
    """ Transforms input array into deque of LZSS nodes
        which are either literal characters or references to previous text.
    """
    in_buf = []
    out = deque()

    char_buf = deque()
    pos = -1
    in_vals = deque(in_arr)

    while len(in_vals) > 0:
        c = in_vals.popleft()
        pos = handle_new_character(c, pos, in_buf, char_buf, out)
        in_buf.append(c)

        if len(in_buf) == buffer_size:
            in_buf = in_buf[1:]
            pos -= 1
            if pos < 0:
                append_lzss_node(out, pos, char_buf, in_buf)
                char_buf.clear()

    if pos >= 0:
        append_lzss_node(out, pos, char_buf, in_buf)

    return out


def parse_text(out: deque[LZSSNode], in_vals: deque[int], n_chars: int):
    """ Reads n char amount of characters from input values
        and transforms them into literal lzss nodes
        and appends them into out.
    """
    for i in range(0, n_chars):
        out.append(LZSSNode(char=in_vals.popleft()))


def parse_ref(out: deque[LZSSNode], in_vals: deque[int], length: int):
    """ Reads distance of the match from input values
        and appends the pair of length and distance as lzss nodes into out
    """
    dist = in_vals.popleft()
    out.append(LZSSNode(length=length, dist=dist))


def lzss_parse(in_arr: bytearray) -> deque[LZSSNode]:
    """ Parses encoded lzss data
        and transforms them into deque of lzss nodes
    """
    out = deque()
    in_vals = deque(in_arr)
    while len(in_vals) > 0:
        # parity of this tells whether the following is text or a ref
        b0 = in_vals.popleft()
        is_ref = b0 % 2 == 1
        # the other 7 bits are length/str_len
        b0 = b0 // 2
        if is_ref:
            parse_ref(out, in_vals, b0)
        else:
            parse_text(out, in_vals, b0)

    return out


def lzss_to_decrypted(in_nodes: deque[LZSSNode]) -> bytearray:
    """ takes lzss nodes as input and transforms them into
        original bytearray
    """
    out = bytearray()
    while len(in_nodes) > 0:
        node = in_nodes.popleft()
        if node.is_literal():
            out.append(node.char)
        else:
            n = len(out)
            for i in range(0, node.length):
                out.append(out[n-node.dist+i])

    return out


def append_with_len(out: bytearray(), in_vals: deque[int]):
    """ Appends literal characters along
        with the number of characters to be appended
    """
    while len(in_vals) > 0:
        len_app = min(127, len(in_vals))
        out.append(len_app*2)
        for i in range(0, len_app):
            out.append(in_vals.popleft())


def lzss_to_encrypted(in_nodes: deque[LZSSNode]) -> bytearray:
    """ Takes lzss nodes as input and transforms them into
        lzss encoded bytearray
    """
    out = bytearray()
    in_vals = deque()
    for node in in_nodes:
        if node.is_literal():
            (val, none) = node.value()
            in_vals.append(val)
        else:
            if len(in_vals) > 0:
                append_with_len(out, in_vals)

            out.append(node.length*2+1)
            out.append(node.dist)

    if len(in_vals) > 0:
        append_with_len(out, in_vals)

    return out


def lzss_encode(in_arr: bytearray, buffer_size: int = 2**8) -> bytearray:
    """ Encodes the input string using LZSS Encoding.
    """
    lzss_lst = to_lzss(in_arr, buffer_size)
    return lzss_to_encrypted(lzss_lst)


def lzss_decode(in_arr: bytearray) -> bytearray:
    """ Decodes the input string using LZSS Decoding.
    """
    lzss_lst = lzss_parse(in_arr)
    return lzss_to_decrypted(lzss_lst)
