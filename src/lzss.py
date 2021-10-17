from collections import deque


def append_text(s: str, bta: bytearray = bytearray()) -> bytearray:
    while len(s) > 127:
        s_len = len(s)
        # multiply by two to set last bit to 0
        len_bytes = (127*2).to_bytes(1, 'big')
        bta += len_bytes + s[:127].encode()
        s = s[127:]

    if len(s) == 0:
        return bta

    s_len = len(s)
    len_bytes = (s_len*2).to_bytes(1, 'big')

    return bta + len_bytes + s.encode()


def append_ref(ref_len: int, ref_pos: int,
               bta: bytearray = bytearray()) -> bytearray:
    # *2+1 to set last bit to 1
    len_bytes = (ref_len*2+1).to_bytes(1, 'big')

    pos_bytes = ref_pos.to_bytes(1, 'big')

    return bta + len_bytes + pos_bytes


def append_lzss(pos: int, s: str, in_buf: deque,
                out_buf: str, out: bytearray) -> (str, bytearray):
    """ Formats the matched string
        into proper form and appends it to the output
    """
    if len(s) >= 2:
        relative_pos = len(in_buf)-pos-len(s)
        out = append_text(out_buf, out)
        out = append_ref(len(s), relative_pos, out)
        return ("", out)
    else:
        return (out_buf + s, out)


def check_match_from(pos: int, s: str, in_buf: deque) -> bool:
    """ Checks if 's' is in 'in_buf' starting from 'pos'
    """
    i = 0
    for i in range(0, len(s)):
        if s[i] != in_buf[pos+i]:
            return False
    return True


def buffer_find(s: str, in_buf: deque) -> int:
    """ Checks if 's' is included in 'in_buf'
        Returns 'pos' of matched string if found,
        otherwise returns -1
    """
    pos = len(in_buf) - len(s)
    while pos >= 0:
        if check_match_from(pos, s, in_buf):
            return pos
        pos -= 1
    return pos


def check_match(c: str, s: str, pos: int, in_buf: deque,
                out_buf: str, out: bytearray) -> (int, str, str, bytearray):
    """ Handles a new character:
        if there is a previous match, checks if the match can be elongated;
        if not, checks if the new character can be matched separately.
        Returns updated output with the information about the current match.
    """
    if pos >= 0:
        new_s = s + c
        new_pos = buffer_find(new_s, in_buf)
        if new_pos >= 0:
            return (new_pos, new_s, out_buf, out)
        else:
            (out_buf, out) = append_lzss(pos, s, in_buf, out_buf, out)

    pos = buffer_find(c, in_buf)
    if pos >= 0:
        return (pos, c, out_buf, out)
    else:
        return (pos, "", out_buf + c, out)


def lzss_encode(input_string: str, buffer_size: int = 2**8-1) -> bytearray:
    """ Encodes the input string using
        Lempel-Ziv-Storer-Szymanski encoding
    """
    in_buf = deque()
    out = bytearray()
    out_buf = ""

    s = ""
    pos = -1

    for i in range(0, len(input_string)):
        c = input_string[i]
        (pos, s, out_buf, out) = check_match(c, s, pos, in_buf, out_buf, out)
        in_buf.append(c)

        if len(in_buf) == buffer_size + 1:
            in_buf.popleft()
            pos -= 1
            if pos < 0:
                (out_buf, out) = append_lzss(pos, s, in_buf, out_buf, out)
                s = ""

    if pos >= 0:
        (out_buf, out) = append_lzss(pos, s, in_buf, out_buf, out)
    out = append_text(out_buf, out)

    return out


def parse_text(str_len: int, bta: bytearray()) -> (str, bytearray):
    text = bta[:str_len].decode('utf-8')
    rest = bta[str_len:]
    return (text, rest)


def parse_ref(ref_len: int, bta: bytearray()) -> (int, int, bytearray):
    ref_pos = bta[0]
    rest = bta[1:]
    return (ref_len, ref_pos, rest)


def lzss_decode(bta: bytearray()) -> str:
    out = ""
    while len(bta) > 0:
        # parity of this tells whether the following is text or a ref
        b0 = bta[0]
        bta = bta[1:]
        is_ref = b0 % 2 == 1
        # the other 7 bits are ref_len/str_len
        b0 = b0 // 2
        if is_ref:
            (ref_len, ref_pos, bta) = parse_ref(b0, bta)
            n = len(out)
            out += out[n-ref_pos:n-ref_pos+ref_len]
        else:
            (text, bta) = parse_text(b0, bta)
            out += text

    return out
