# seglines

**What:**

Compute segmented least squares for a dataset.  Probably assumes that `X = 1...N` or something.

**Install:**

`pip install seglines`

**Usage:**

`seglines l data.csv`



To generate data first:

`seglines --generate 5 10 > data.csv`

and then

`seglines 5 data.csv`

This outputs the segments, and also writes a file `data.csv` for your convenience.
