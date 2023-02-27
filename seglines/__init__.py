import sys
import csv
from ._version import __version__ as version
from .generator import generate
from .segmentedls import solve, plot


def _read(fname):
    data = []
    with open(fname, "r", encoding="utf8") as fin:
        csvreader = csv.reader(fin)
        for row in csvreader:
            x, y = map(float, row)
            data.append((x, y))
    return data


def _slope_to_str(slope):
    a, b = slope
    return f"f(x) = {a:.3f}·x + {b:.3f}"


def run(fname, L, do_plot=False):
    data = _read(fname)
    X, Y = zip(*data)
    OPT = solve(X, Y, L)
    if do_plot:
        plot(OPT, X, Y, L, fname.split(".")[0])

    N = len(X)

    l = L
    i = len(X)

    opt = OPT[l, i]
    print(f"opt = {opt.opt:.2f}")

    segments = []

    digits_ = len(str(i))

    while opt.l > 0:
        x1, y1 = opt.pre, Y[max(0, opt.pre)]
        x2, y2 = opt.i - 1, Y[max(0, opt.i - 1)]
        segments.append(((x1, round(y1, 2)), (x2, round(y2, 2)), opt.slope))
        opt = OPT[opt.l - 1, opt.pre]

    for idx, (start, end, slope) in enumerate(reversed(segments)):
        s, s_val = start
        e, e_val = end
        slope_str = _slope_to_str(slope)
        print(f"segment {idx+1:2}: ", end="")
        print(f"{s:{digits_}} ({s_val:.3f})".ljust(digits_ + 13), end="")
        print(f"{e:{digits_}} ({e_val:.3f})".ljust(digits_ + 13), end="")
        print(slope_str)


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

    do_plot = False
    if "--plot" in args:
        do_plot = True
        args.remove("--plot")

    if len(args) != 3:
        exit_with_usage(error=1)
    L = int(args[1])
    run(args[2], L, do_plot=do_plot)


if __name__ == "__main__":
    main()
