from heapq import heappush, heappop, heapify


class HuffTree:
    def __init__(self, char: str, count: int):
        self.char = char
        self.count = count
        self.left = None
        self.right = None

    def merge(self, other):
        first = HuffTree(self.char, self.count)
        first.left = self.left
        first.right = self.right
        self.char = None
        self.count = first.count + other.count
        self.left = first
        self.right = other

    def __str__(self):
        if self.char is not None:
            return f"{self.count} {self.char}"
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


def dict_increment(d: dict, newchar: str) -> dict:
    if newchar in d:
        d[newchar] += 1
    else:
        d[newchar] = 1
    return d

# lambda item: 2*item
# lambda x: 2*x
# f(x) 2*x

def counts(input_string: str) -> list:
    d = {}
    for s in input_string:
        dict_increment(d, s)
    hufftree_list = list(map(lambda item: HuffTree(item[0], item[1]), d.items()))
    return hufftree_list


def counts_to_heap(lst: list) -> list:
    heapify(lst)
    return lst


def heap_to_hufftree(h: list) -> HuffTree:
    while len(h) > 1:
        node1 = heappop(h)
        node2 = heappop(h)
        node1.merge(node2)
        heappush(h, node1)

    return heappop(h)


def hufftree_to_keys(ht: HuffTree, prefix: str) -> list:
    if ht.char is not None:
        return [(ht.char, prefix)]
    else:
        left = hufftree_to_keys(ht.left, prefix + "0")
        right = hufftree_to_keys(ht.right, prefix + "1")
        return left + right


def huff_encode(input_string: str) -> str:

    counts_dict = counts(input_string)
    heapify_dict = counts_to_heap(counts_dict)
    make_it_hufftree = heap_to_hufftree(heapify_dict)
    keys = hufftree_to_keys(make_it_hufftree, "")

    key_dict = {}

    output_string = ""
    for key, value in keys:
        key_dict[key] = value
        output_string += key + ":" + value + " "

    output_string += "| "

    for char in input_string:
        output_string += key_dict[char]

    return output_string


def parse_huffman_tree(input_string: str) -> (dict, str):

    key_dict = {}

    i = 0
    current_char = input_string[0]
    while current_char != "|":
        i += 2 # skip colon

        key = ""
        while input_string[i] != " ":
            key += input_string[i]
            i += 1 # move to next number

        key_dict[key] = current_char
        i += 1 # skip space
        current_char = input_string[i]

    return (key_dict, input_string[(i+2):])


def huff_decode(input_string: str) -> str:
    (key_dict, encoded_string) = parse_huffman_tree(input_string)

    i = 0
    decoded_string = ""
    while i < len(encoded_string):
        current_key = encoded_string[i]
        while current_key not in key_dict:
            i += 1
            current_key += encoded_string[i]
        decoded_string += key_dict[current_key]

        i += 1

    return decoded_string