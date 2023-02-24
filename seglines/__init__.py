from .generator import generate
from .segmentedls import run


def main():
    import sys

    if len(sys.argv) == 4 and sys.argv[1] == "--generate":
        L, K = map(int, sys.argv[2:])
        N = L * K
        generate(L, K, N)
        exit()

    if len(sys.argv) != 3:
        exit(
            "usage: seglines L myfile.csv (L is number of segments)\n"
            + "usage: seglines --generate k l"
        )
    L = int(sys.argv[1])
    run(sys.argv[2], L)
