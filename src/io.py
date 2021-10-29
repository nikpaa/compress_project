from deflate import defl_encode, defl_decode
import sys


def deflate_file(input_filename: str):
    output_filename = input_filename + '.defl'
    input_data = bytearray()
    with open(input_filename, 'rb') as f:
        byte = f.read(1)
        while byte:
            input_data.append(int.from_bytes(byte, 'big'))
            byte = f.read(1)
    deflated_data = defl_encode(input_data)
    out_file = open(output_filename, 'wb')
    out_file.write(deflated_data)
    out_file.close()


def inflate_file(output_filename: str):
    input_filename = output_filename + '.defl'
    deflated_data = bytearray()
    of2 = output_filename + '.infl'
    with open(input_filename, 'rb') as f:
        byte = f.read(1)
        while byte:
            deflated_data.append(int.from_bytes(byte, 'big'))
            byte = f.read(1)

    inflated_data = defl_decode(deflated_data)
    out_file = open(of2, 'wb')
    out_file.write(inflated_data)
    out_file.close()


deflate_file(sys.argv[1])
inflate_file(sys.argv[1])
