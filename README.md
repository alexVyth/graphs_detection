# Graph top-k Link Detection

## Installation

Python 3.9.1 was used. To install dependencies run:

    pip install -r requirements

## Usage

To get usage help run:

    python3 main.py --help

## Example

Running:

    python3 main.py -d ./data/ca-GrQc.txt -r AL -m adamic-adar -k 10

Outputs:

    Representation=AL, Metric=adamic-adar, k=10

    Top-k Results:
    #   Score   Edge
    1   10.60   (45, 46)
    2   10.59   (4511, 22691)
    3   10.59   (4511, 4513)
    4   10.34   (46, 22691)
    5   10.34   (46, 4513)
    6   6.70    (7444, 15245)
    7   6.70    (7444, 12710)
    8   6.70    (7444, 9869)
    9   6.70    (7444, 8727)
    10  6.70    (5210, 7444)
    
    Finished in 18.0 seconds.
