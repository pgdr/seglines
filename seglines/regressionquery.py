from collections import namedtuple as T

RegressionState = T(
    "RegressionState",
    "a b n sum_x sum_y sum_xy sum_x2 sum_y2 a_nom denom b_nom sse",
)


def _axb(state, r=5):
    """Print s.a and s.b as "a·x+b"."""
    a = round(state.a, r)
    b = round(state.b, r)
    if b >= 0:
        return f"{a}·x + {b} ({state.n} points)"
    return f"{a}·x - {-b} ({state.n} points)"


RegressionState.__str__ = _axb
RegressionState.slope = lambda s: (s.a, s.b)


def _regression(x, y, state=None):
    if state is None or state.n == 0:
        n = 1
        sum_x = x
        sum_y = y
        sum_xy = x * y
        sum_x2 = x * x
        sum_y2 = y * y
    else:
        n = state.n + 1
        sum_x = state.sum_x + x
        sum_y = state.sum_y + y
        sum_xy = state.sum_xy + x * y
        sum_x2 = state.sum_x2 + x * x
        sum_y2 = state.sum_y2 + y * y

    a_nom = n * sum_xy - sum_x * sum_y
    denom = n * sum_x2 - sum_x * sum_x
    b_nom = sum_y * sum_x2 - sum_x * sum_xy

    if denom == 0:
        a = 0.0
        b = sum_y / n
    else:
        a = a_nom / denom
        b = b_nom / denom

    sse = (
        sum_y2
        - 2 * a * sum_xy
        - 2 * b * sum_y
        + (a * a) * sum_x2
        + 2 * a * b * sum_x
        + (b * b) * n
    )

    return RegressionState(
        a,
        b,
        n,
        sum_x,
        sum_y,
        sum_xy,
        sum_x2,
        sum_y2,
        a_nom,
        denom,
        b_nom,
        sse,
    )


def build_query(X, Y):
    N = len(X)
    DP = {}
    DP[(0, 0)] = _regression(X[0], Y[0])
    for i in range(1, N + 1):
        DP[(i, i)] = _regression(X[i - 1], Y[i - 1])

    for i in range(0, N + 1):
        for j in range(i + 1, N + 1):
            DP[(i, j)] = _regression(
                X[j - 1], Y[j - 1], DP[(i, j - 1)]
            )
    return DP
