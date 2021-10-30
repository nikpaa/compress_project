# Performance testing

The data is obtained with the following commands:

```bash
for f in {200,400,600,800,1000,1200}; do head -c $f data/dostoyevski_100.txt > data/dost$f.txt; done
for f in {200,400,600,800,1000,1200}; do time python3 src/io.py deflate data/dost$f.txt; done
```

## Time

Here are some measurements for processing times of deflating a file of 200, 400, 600, 800, 1000 and 1200 bytes:

```bash
python3 src/io.py deflate data/dost$f.txt  0,03s user 0,01s system 82% cpu 0,052 total
python3 src/io.py deflate data/dost$f.txt  0,04s user 0,01s system 90% cpu 0,051 total
python3 src/io.py deflate data/dost$f.txt  0,05s user 0,01s system 91% cpu 0,068 total
python3 src/io.py deflate data/dost$f.txt  0,07s user 0,01s system 93% cpu 0,087 total
python3 src/io.py deflate data/dost$f.txt  0,09s user 0,01s system 95% cpu 0,106 total
python3 src/io.py deflate data/dost$f.txt  0,12s user 0,01s system 95% cpu 0,138 total
```
