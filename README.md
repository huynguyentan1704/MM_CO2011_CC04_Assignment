# TASK 1 BTL MHH

**Reading Petri nets from PNML files**: Implement a parser that reads a 1-safe Petri
net from a standard PNML file1 and constructs the internal representation of places,
transitions, and flow relations. The program should verify consistency (e.g., no missing
arcs or nodes).

https://www.pnml.org/version-2009/version-2009.php

## Requirements

- Python 3+
- numpy
- pytest
.....

##  Running tests

- Run all tests
```
pytest test_petriNet.py -vv
```

- Run a single test function

```
pytest test_petriNet.py -vv
```