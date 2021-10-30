# Compress project

Algorithms and data structures project

## Documentation

* [Implementation](documentation/implementation.md)
* [Some examples of running time](documentation/performance.md)

## Progress reports

* [Week 1](documentation/progress_report_week1.md)
* [Week 2](documentation/progress_report_week2.md)
* [Week 3](documentation/progress_report_week3.md)
* [Week 4](documentation/progress_report_week4.md)
* [Week 5](documentation/progress_report_week5.md)
* [Week 6](documentation/progress_report_week6.md)
* [Week 7](documentation/progress_report_week7.md)

## Commands

### Testing

Tests are done using the command:

```bash
pytest src
```

### Test Coverage Report

This project uses coveragerc for code coverage report.
Test coverage report can be generated using the command:

```bash
coverage run --branch -m pytest src
```

### Linting

Pylint report can be obtained using the command:

```bash
pylint src
```

### Example

Files can be compressed as follows:

```bash
python3 src/io.py deflate data/dostoyevski_100.txt
# output is in the file data/dostoyevski_100.txt.defl
```

Decompression works like so:
```bash
# note that the input file should not include the .defl file extension
python3 src/io.py inflate data/dostoyevski_100.txt
# output is in the file data/dostoyevski_100.txt.infl
```
