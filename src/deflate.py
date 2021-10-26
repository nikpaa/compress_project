from collections import deque
from huffman import get_codes, read_code, read_code_dict, append_vals, rle
from lzss import to_lzss, LZSSNode, lzss_to_decrypted
from helpers import bits_to_int, clear_buf, int_to_min_bits, read_to_buf


def write_node_to_buf(in_nodes: list[LZSSNode],
                      sym_codes: list[list[int]], dist_codes: list[list[int]],
                      out: bytearray, out_buf: deque[int]):
    """ Puts an LZSS node into buffer.
    """
    node = in_nodes.popleft()
    append_vals(out_buf, sym_codes[node.defl_sym()])
    if not node.is_literal():
        append_vals(out_buf, int_to_min_bits(node.length))
        append_vals(out_buf, dist_codes[node.defl_dist()])
        append_vals(out_buf, int_to_min_bits(node.dist))


def defl_encode(input_bytes: bytearray) -> bytearray:
    """ Encodes the data using Deflate-algorithm
    """
    in_nodes = to_lzss(input_bytes, 2**15)
    in_nodes.append(LZSSNode(char=256))
    sym_values = [node.defl_sym() for node in in_nodes]

    (sym_code_lens, sym_codes) = get_codes(sym_values, 288)

    dist_values = [d.defl_dist() for d in in_nodes if not d.is_literal()]
    (dist_code_lens, dist_codes) = get_codes(dist_values, 32)

    out = bytearray()

    # add rle bitlengths
    out += rle(sym_code_lens)
    out += rle(dist_code_lens)

    # add input data
    out_buf = deque([])
    while len(in_nodes) > 0:
        write_node_to_buf(in_nodes, sym_codes, dist_codes, out, out_buf)
        clear_buf(out, out_buf, 7)

    # add rest of the buffer
    clear_buf(out, out_buf, 0)

    return out


def parse_ref(out: deque[LZSSNode], code: int, dist_codes: dict[str, int],
              in_vals: deque[int], in_buf: deque[str]):
    """ Parses an LZSS reference and appens it to output as LZSS node.
    """
    # parse sym
    sym_bits = code - 255
    read_to_buf(in_vals, in_buf, sym_bits)
    length = []
    for i in range(0, sym_bits):
        length.append(int(in_buf.popleft()))
    # parse dist
    dist_bits = read_code(in_vals, in_buf, dist_codes)
    read_to_buf(in_vals, in_buf, dist_bits)
    dist = []
    for i in range(0, dist_bits):
        dist.append(int(in_buf.popleft()))
    out.append(LZSSNode(length=bits_to_int(length),
                        dist=bits_to_int(dist)))


def defl_parse(in_arr: bytearray) -> deque[LZSSNode]:
    """ Parses a deque of LZSS nodes out of input array
    """
    in_vals = deque(in_arr)

    sym_codes = read_code_dict(in_vals, 288)
    dist_codes = read_code_dict(in_vals, 32)

    out = deque([])
    in_buf = deque([])
    code = read_code(in_vals, in_buf, sym_codes)
    while code != 256:
        if code < 256:
            out.append(LZSSNode(char=code))
        else:
            parse_ref(out, code, dist_codes, in_vals, in_buf)

        code = read_code(in_vals, in_buf, sym_codes)

    return out


def defl_decode(in_arr: bytearray) -> bytearray:
    """ Decodes data that was compressed using Deflate-algorithm
    """
    return lzss_to_decrypted(defl_parse(in_arr))

