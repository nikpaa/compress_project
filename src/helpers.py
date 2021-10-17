# transforms bits to byte type
# only works for length <= 8
def bits_to_byte(bits: list[int]) -> bytes:
    output = 0
    for i in range(0, len(bits)):
        output += 2**i * bits[i]

    return output.to_bytes(1, 'big')

# transforms integer to list of bits
# only works correctly for integers up to 255
def int_to_bits(b: int) -> list[int]:
    output = []
    for i in range(0, 8):
        output.append(b % 2)
        b = b // 2

    return output

# transforms list of bits to string of bits
def bits_to_str(lst: list) -> str:
    output = ""
    for i in lst:
        output += str(i)
    return output

# composes two previous functions
def int_to_bit_str(b: int) -> list[int]:
    return bits_to_str(int_to_bits(b))


""" RLE implementation

    Assumes that the elements of 'bit_lengths' list are integers between 0 and 255
"""
def rle(bit_lengths: list[int]) -> bytearray:
    current = bit_lengths[0]
    current_count = 1
    output = bytearray()
    for i in range(1, len(bit_lengths)):

        # next byte matches current byte
        if current_count < 255 and bit_lengths[i] == current:
            current_count += 1
        # next byte differs, append current byte along with its count to output and
        # set new current byte and current count
        else:
            output += current_count.to_bytes(1, 'big')
            output += current.to_bytes(1, 'big')
            current = bit_lengths[i]
            current_count = 1

    # append last byte along with its count
    output += current_count.to_bytes(1, 'big')
    output += current.to_bytes(1, 'big')

    return output
