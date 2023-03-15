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
