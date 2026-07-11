"""
trend_tests.py
==============
Non-parametric trend tests for Variable 2 (Cloud Infrastructure Concentration).

Implements the Mann-Kendall trend test and Sen's slope estimator from first
principles (no external trend-test dependency), suited to the short annual HHI
series (n=7, 2017-2023). These are reported alongside OLS because non-parametric
trend tests do not assume normality or linearity and are the standard choice for
small annual time series.

Run:  python trend_tests.py
"""

import numpy as np
from itertools import combinations
from scipy import stats

# HHI series, 2017-2023. 2024 excluded (Synergy Azure IaaS/PaaS -> SaaS reclassification).
YEARS = np.array([2017, 2018, 2019, 2020, 2021, 2022, 2023])
HHI   = np.array([1269, 1307, 1378, 1442, 1531, 1611, 1658])


def mann_kendall(x):
    """Mann-Kendall trend test with continuity correction. Returns dict."""
    n = len(x)
    S = sum(np.sign(x[j] - x[i]) for i, j in combinations(range(n), 2))
    # Variance assuming no ties (verified: HHI series has no repeated values)
    var_S = n * (n - 1) * (2 * n + 5) / 18
    if S > 0:
        Z = (S - 1) / np.sqrt(var_S)
    elif S < 0:
        Z = (S + 1) / np.sqrt(var_S)
    else:
        Z = 0.0
    p = 2 * (1 - stats.norm.cdf(abs(Z)))
    tau = S / (0.5 * n * (n - 1))
    return {"S": S, "var_S": var_S, "Z": Z, "tau": tau, "p": p, "n": n}


def sens_slope(x, t):
    """Sen's (Theil-Sen) slope estimator. Returns (slope, intercept)."""
    slopes = [(x[j] - x[i]) / (t[j] - t[i])
              for i, j in combinations(range(len(x)), 2)]
    slope = np.median(slopes)
    intercept = np.median(x) - slope * np.median(t)
    return slope, intercept, len(slopes)


if __name__ == "__main__":
    mk = mann_kendall(HHI)
    sen_slope, sen_int, n_pairs = sens_slope(HHI, YEARS)
    ols = stats.linregress(YEARS, HHI)

    print("Mann-Kendall trend test (HHI, 2017-2023)")
    print(f"  S statistic     : {mk['S']}")
    print(f"  Kendall's tau   : {mk['tau']:.4f}")
    print(f"  Z (cont. corr.) : {mk['Z']:.4f}")
    print(f"  p-value (2-tail): {mk['p']:.5f}")
    print(f"  n               : {mk['n']}")
    print()
    print("Sen's slope estimator")
    print(f"  Sen's slope     : {sen_slope:.2f} HHI/year")
    print(f"  pairwise slopes : {n_pairs}")
    print()
    print("OLS (reported for comparison)")
    print(f"  OLS slope       : {ols.slope:.2f} HHI/year")
    print(f"  R-squared       : {ols.rvalue**2:.4f}")
    print(f"  p-value         : {ols.pvalue:.6f}")
