import numpy as np
from collections import defaultdict as D
from collections import namedtuple as T

Solution = T("Solution", "opt i l pre slope")


def sol(opt, i, l, pre, slope):
    return Solution(opt, i, l, pre, slope)  # please never round


sol0 = sol(0, 0, 0, 0, None)
VINF = sol(float("inf"), 0, 0, 0, None)


def _lstsq(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    lstsq = np.linalg.lstsq(A, y, rcond=None)
    lstsq_sol = lstsq[0]
    residuals = lstsq[1]
    return np.sum(residuals), lstsq_sol


def segmented_least_squares(X, Y, L):
    OPT = D(lambda: VINF)

    ## Base case for one line
    for i in range(len(X) + 1):
        sse, lstsol = _lstsq(X[:i], Y[:i])
        OPT[1, i] = sol(sse, i, 1, 0, lstsol)

    ## Base for 1 point
    for l in range(2, L + 1):
        OPT[l, 0] = sol0

    ## recurrence:
    ## ## for number of segments l = 1 ... L
    ## ## ### for number of points i = 1 ... n
    for l in range(1, L + 1):
        for i in range(1, len(X) + 1):
            for j in range(0, i - 1):
                sse, lstsol = _lstsq(X[j:i], Y[j:i])  # cost of line from j to i
                pre = OPT[l - 1, j]  # one fewer line, ending at j
                this = pre.opt + sse
                if this < OPT[l, i].opt:
                    OPT[l, i] = sol(this, i, l, j, lstsol)
    return OPT


def plot(OPT, X, Y, L, fname):
    import matplotlib.pyplot as plt
    XMIN = -1
    XMAX = len(X) + 1
    YMIN = -5
    YMAX = max(Y) + 5
    l = L
    i = len(X)
    opt = OPT[l, i]
    plt.xlim(XMIN, XMAX)
    plt.ylim(YMIN, YMAX)
    _opt_str = f"{round(opt.opt,1)}"
    label = f"L={l}, i={i}, opt={_opt_str.ljust(8)}"
    plt.plot(X[:i], Y[:i], "o", markersize=4, c="blue", label=label)
    plt.plot(X[i:], Y[i:], "o", markersize=2, c="black")
    plt.legend(loc="upper right")
    while opt.l > 0:
        x1, y1 = opt.pre, Y[max(0, opt.pre)]
        x2, y2 = opt.i - 1, Y[max(0, opt.i - 1)]
        plt.plot((x1, x2), (y1, y2))
        opt = OPT[opt.l - 1, opt.pre]

    plt.savefig(f"{fname}.png")


def solve(X, Y, L):
    OPT = segmented_least_squares(X, Y, L)
    return OPT
