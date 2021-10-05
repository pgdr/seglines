import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict as D
from collections import namedtuple as T
from pprint import pprint
import random

V = T("V", "opt m c i l pre")
V0 = V(0, 0, 0, 0, 0, 0)
VINF = V(float("inf"), 0, 0, 0, 0, 0)


L = 6
k = 20
N = L * k

X = np.array(range(N))
_yarr = list(range(1, k + 1))
_act_y = []
for i in range(L):
    tmp = []
    offset = random.randint(1, 5)
    for e in _yarr:
        tmp.append(random.gauss(offset + e, 0.8))
    if random.random() > 0.5:
        tmp = reversed(tmp)
    _act_y += tmp
Y = np.array(_act_y)
print("Y = " + " ".join([str(round(e, 1)) for e in list(Y)]))

OPT = D(lambda: VINF)

for i in range(N + 1):
    x = X[:i]
    y = Y[:i]
    A = np.vstack([x, np.ones(len(x))]).T
    lstsq = np.linalg.lstsq(A, y, rcond=None)
    m, c = lstsq[0]
    residuals = lstsq[1]
    SSE = np.sum(residuals)
    OPT[1, i] = V(SSE, m, c, i, 1, 0)

for l in range(2, L + 1):
    for i in range(1 + 2 * l):
        OPT[l, i] = V0


for l in range(1, L + 1):
    for i in range(1, N + 1):
        if i < (1 + 2 * l):
            continue
        for j in range(0, i - 1):
            x = X[j:i]
            y = Y[j:i]
            A = np.vstack([x, np.ones(len(x))]).T
            lstsq = np.linalg.lstsq(A, y, rcond=None)
            m, c = lstsq[0]
            residuals = lstsq[1]
            SSE = np.sum(residuals)

            pre = OPT[l - 1, j]
            this = pre.opt + SSE
            if this < OPT[l, i].opt:
                OPT[l, i] = V(this, m, c, i, l, j)

XMIN = -1
XMAX = N + 1
YMIN = -5
YMAX = max(Y) + 5
counter = 0
for l in range(1, L + 1):
    for i in range(1, N + 1):
        print(l, i, OPT[l, i])
        opt = OPT[l, i]
        plt.clf()
        hasplot = False
        plt.xlim(XMIN, XMAX)
        plt.ylim(YMIN, YMAX)
        _opt_str = f"{round(opt.opt,1)}"
        label = f"L={l}, i={i}, opt={_opt_str.ljust(8)}"
        plt.plot(X[:i], Y[:i], "o", markersize=4, c="blue", label=label)
        plt.plot(X[i:], Y[i:], "o", markersize=2, c="black")
        plt.legend(loc="upper right")
        while opt.l > 0:
            plt.plot(X, opt.m * X + opt.c, "r--")  # TODO linesegment
            opt = OPT[opt.l - 1, opt.pre]
            hasplot = True

        if hasplot:
            counter += 1
            plt.savefig(f"abc{counter:03d}.png")
