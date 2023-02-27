import sys
import csv
from ._version import __version__ as version
from .generator import generate
from .segmentedls import solve, plot


def _read(fname):
    data = []
    with open(fname, "r") as fin:
        csvreader = csv.reader(fin)
        for row in csvreader:
            x, y = map(float, row)
            data.append((x, y))
    return data


def run(fname, L):
    data = _read(fname)
    X, Y = zip(*data)
    OPT = solve(X, Y, L)
    plot(OPT, X, Y, L, fname.split(".")[0])


def exit_with_usage(error=0):
    print("seglines\n\nCompute segmented least squares on your dataset.\n")
    print("usage: seglines L myfile.csv (L is number of segments)")
    print("       seglines L myfile.csv --plot")
    print("       seglines --generate k l")
    print("       seglines --help")
    print("       seglines --version")
    sys.exit(error)


def main():
    args = [e for e in sys.argv]
    print(args)

    if "-h" in args or "--help" in args:
        exit_with_usage()

    if "-v" in args or "--version" in args:
        print("seglines", version)
        sys.exit()

    if len(args) == 4 and args[1] == "--generate":
        L, K = map(int, args[2:])
        N = L * K
        generate(L, K, N)
        sys.exit()

    plot = False
    if "--plot" in args:
        plot = True
        args.remove("--plot")

    if len(args) != 3:
        exit_with_usage(error=1)
    L = int(args[1])
    run(args[2], L)


if __name__ == "__main__":
    main()
