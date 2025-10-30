from collections import defaultdict as D
from collections import namedtuple as T
from .regressionquery import build_query

Solution = T("Solution", "opt i k pre slope")


def sol(opt, i, k, pre, slope):
    return Solution(opt, i, k, pre, slope)  # please never round


sol0 = sol(0, 0, 0, 0, None)
VINF = sol(float("inf"), 0, 0, 0, None)


def query(dp, i, j):
    state = dp[(i, j)]
    return state.sse, state.slope()


def segmented_least_squares(X, Y, L):
    DP = build_query(X, Y)
    OPT = D(lambda: VINF)

    ## Base case for one line
    for i in range(len(X) + 1):
        sse, slope = query(DP, 0, i)
        OPT[1, i] = sol(sse, i, 1, 0, slope)

    ## Base for 1 point
    for k in range(2, L + 1):
        OPT[k, 0] = sol0

    ## recurrence:
    ## ## for number of segments k = 1 ... L
    ## ## ### for number of points i = 1 ... n
    for k in range(1, L + 1):
        for i in range(1, len(X) + 1):
            for j in range(0, i - 1):
                sse, slope = query(
                    DP, j, i
                )  # cost of line from j to i
                pre = OPT[k - 1, j]  # one fewer line, ending at j
                this = pre.opt + sse
                if this < OPT[k, i].opt:
                    OPT[k, i] = sol(this, i, k, j, slope)
    return OPT


def solve(X, Y, L):
    OPT = segmented_least_squares(X, Y, L)
    return OPT
