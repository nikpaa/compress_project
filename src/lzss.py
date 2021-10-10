from collections import deque


def append_lzss(output: str, pos: int, s: str, buf: deque) -> str:
    """ Formats the matched string
        into proper form and appends it to the output
    """
    if len(s) >= 2:
        relative_pos = str(len(buf)-pos-len(s))
        output += "<" + relative_pos + "," + str(len(s)) + ">"
    else:
        output += s
    return output


def check_match_from(pos: int, s: str, buf: deque) -> bool:
    """ Checks if 's' is in 'buf' starting from 'pos'
    """
    i = 0
    for i in range(0, len(s)):
        if s[i] != buf[pos+i]:
            return False
    return True


def buffer_find(s: str, buf: deque) -> int:
    """ Checks if 's' is included in 'buf' 
        Returns 'pos' of matched string if found,
        otherwise returns -1
    """
    pos = len(buf) - len(s)
    while pos >= 0:
        if check_match_from(pos, s, buf):
            return pos
        pos -= 1
    return pos


def check_match(c: str, s: str, pos: int, buf: deque, output: str) -> (int, str, str):
    """ Handles a new character:
        if there is a previous match, checks if the match can be elongated;
        if not, checks if the new character can be matched separately.
        Returns the updated output with the information about the current match.
    """
    if pos >= 0:
        new_s = s + c
        new_pos = buffer_find(new_s, buf)
        if new_pos >= 0:
            return (new_pos, new_s, output)
        else:
            output = append_lzss(output, pos, s, buf)    
    
    pos = buffer_find(c, buf)
    if pos >= 0:
        return (pos, c, output)
    else:
        return (pos, "", output + c)


def lzss_encode(input_string: str, buffer_size: int = 20) -> str:
    """ Encodes the input string using
        Lempel-Ziv-Storer-Szymanski encoding

        Currently does not work properly if the input_string contains '<'.
    """
    buf = deque()
    output = ""

    s = ""
    pos = -1

    for i in range(0, len(input_string)):
        c = input_string[i]
        (pos, s, output) = check_match(c, s, pos, buf, output)
        buf.append(c)

        if len(buf) == buffer_size + 1:
            buf.popleft()
            pos -= 1
            if pos < 0:
                output = append_lzss(output, pos, s, buf)
                s = ""

    if pos >= 0:
        output = append_lzss(output, pos, s, buf)

    return output


def handle_encoded_str(input_string: str, i: int, output: str) -> (int, str):
    """ Decodes LZSS bracket expression
        to a string, also updates the position
        accordingly.
    """
    i = i+1  # skip opening bracket

    rel_starting_pos_str = ""
    while input_string[i] != ",":
        rel_starting_pos_str += input_string[i]
        i = i+1

    i = i+1  # skip comma

    length_str = ""
    while input_string[i] != ">":
        length_str += input_string[i]
        i = i+1

    i = i + 1  # skip closing bracket

    rel_starting_pos = int(rel_starting_pos_str)
    length = int(length_str)
    starting_pos = len(output)-rel_starting_pos

    encoded_string = output[starting_pos:(starting_pos+length)]

    return (i, output+encoded_string)


def lzss_decode(input_string: str) -> str:
    """ Decodes an LZSS encoded string

        Does not work properly if the original string contained '<'.
    """
    i = 0
    output = ""
    while i < len(input_string):
        if input_string[i] == "<":
            (i, output) = handle_encoded_str(input_string, i, output)
        else:
            output += input_string[i]
            i += 1

    return output