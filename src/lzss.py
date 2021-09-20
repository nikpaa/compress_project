def construct_longer_string(buf: str, current_pos: int, current_len: int, new_char: str) -> str:
    """ Reads the current match from the buffer
        and appends the new character to it.
    """
    return buf[current_pos:(current_pos+current_len)] + new_char


def append_lzss(string: str, pos: int, length: int, buf: str) -> str:
    """ Formats the matched string
        into proper form and appends it to the output
    """
    if length >= 2:
        string += "<" + str(pos) + "," + str(length) + ">"
    else:
        string += buf[pos:(pos+length)]
    return string


def found_new_letter_match(new_char: str, buf: str, output: str) -> (int, int, str):
    """ If a new matching is found, updates the variables
        position, length and output.
    """
    new_char_pos = buf.find(new_char)
    if new_char_pos >= 0:
        return (new_char_pos, 1, output)
    else:
        return (-1, 0, output+new_char)


def handle_new_character(new_char: str, current_pos: int, current_len: int, buf: str, output: str) -> (int, int, str):
    """ Handles a new character:
        if there is a previous match, checks if the match can be elongated;
        if not, checks if the new character can be matched separately.

        Returns the updated output with the information about the current match.
    """
    # earlier match exists
    if current_len > 0:
        # is there a longer match
        new_string = construct_longer_string(buf, current_pos, current_len, new_char)
        new_string_pos = buf.find(new_string)

        # yes
        if new_string_pos >= 0:
            return (new_string_pos, current_len+1, output)
        # no
        else:
            output = append_lzss(output, current_pos, current_len, buf)
            return found_new_letter_match(new_char, buf, output)
    # earlier match does not exist
    else:
        return found_new_letter_match(new_char, buf, output)


def lzss_encode(input_string: str) -> str:
    """ Encodes the input string using
        Lempel-Ziv-Storer-Szymanski encoding

        Currently does not work properly if the input_string contains '<'.
    """
    buffer_string = ""
    output = ""

    current_pos = -1
    current_len = 0

    for s in input_string:
        (current_pos, current_len, output) =\
            handle_new_character(s, current_pos, current_len, buffer_string, output)
        buffer_string += s

    if current_pos >= 0:
        output = append_lzss(output, current_pos, current_len, buffer_string)

    return output


def handle_encoded_str(input_string: str, i: int, output: str) -> (int, str):
    """ Decodes LZSS bracket expression
        to a string, also updates the position
        accordingly.
    """
    i = i+1  # skip opening bracket

    starting_pos_str = ""
    while input_string[i] != ",":
        starting_pos_str += input_string[i]
        i = i+1

    i = i+1  # skip comma

    length_str = ""
    while input_string[i] != ">":
        length_str += input_string[i]
        i = i+1

    i = i + 1  # skip closing bracket

    starting_pos = int(starting_pos_str)
    length = int(length_str)

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
