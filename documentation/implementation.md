# Implementation

## Definition

The purpose of this project is to implement and benchmark DEFLATE -algorithm with Python.

Apparently the implementation of DEFLATE in zlib [has linear time complexity](https://stackoverflow.com/questions/39654986/time-complexity-of-zlibs-deflate-algorithm) so the target of this project is to achieve linear time complexity as well.

For the purposes of reviewing, I'm a CS student and only know python.


## Deflate
The algorithm uses Lempel-Ziv-Storer-Szymanski -algorithm to encode the data and then it uses Huffman Coding to encode the LZSS encoded data. After the data is encoded with LZSS and consists of literal bytes and references to previous text (ie. distance-length-pairs), these objects are huffman encoded in proportion to their frequency. Due to time limits, this implementation differs from the actual [Deflate](https://github.com/madler/zlib) implementation at least with the following ways:

- The compressed data has only one dynamically encoded huffman block rather than multiple blocks with different compression types.
- The distance-length-pairs differ from original implementation. In this implementation, the match codes only contain the information about the bit length of the match and distance codes instead of also containing information about the match length and distance.

### Relevant time complexities
#### Huffman

- Calculating symbol counts for the Huffman tree is `O(n)` with respect to the data length in bytes.
- Constructing the Huffman tree uses [heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) and is `O(nlogn)`. In practice this is infinitesimal because the dictionary size is fixed (288) with respect to the data.
- The Huffman codes are stored in a hash map and accessing them is `O(1)` so encoding the entire data is `O(n)` with respect to the data length.

#### LZSS

Most complex operation is constantly looking back incase the current bytes have previously appeared (`O(ld)`), where `l` is maximum match length, and `d` is maximum match distance (buffer size). For the entire file of length `n` bytes this is `O(nld)`. Because the match length and distance are 2^8 and 2^15, this dominates the entire algorithm's time complexity. Furthermore profiling shows that with files of moderate size eg. 700 KB this takes ~99% of the processing time.

### Space complexity

The current implementation reads the entire data into memory before doing anything so the space complexity is `O(n)` with respect to the data length.

## Sources

* [LZSS](en.wikipedia.org/wiki/Lempel–Ziv–Storer–Szymanski)
* [Huffman Coding](https://en.wikipedia.org/wiki/Huffman_coding)
* [DEFLATE](https://en.wikipedia.org/wiki/Deflate)
* [zlib](https://github.com/madler/zlib)
* [Elegance of deflate](http://www.codersnotes.com/notes/elegance-of-deflate)
