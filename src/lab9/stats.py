"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    tp = fp = fn = tn = 0
    for h, j in zip(human, judge):
        h_fail = (h == POS)
        j_fail = (j == POS)
        if h_fail and j_fail:
            tp += 1
        elif not h_fail and j_fail:
            fp += 1
        elif h_fail and not j_fail:
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    tp, fp, fn = cm["tp"], cm["fp"], cm["fn"]
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    n = len(human)
    if n == 0:
        raise ValueError("Cannot calculate Cohen's kappa for empty sequences")
    cm = confusion(human, judge)
    p_o = (cm["tp"] + cm["tn"]) / n
    p_judge_pos = (cm["tp"] + cm["fp"]) / n
    p_human_pos = (cm["tp"] + cm["fn"]) / n
    p_judge_neg = (cm["fn"] + cm["tn"]) / n
    p_human_neg = (cm["fp"] + cm["tn"]) / n
    p_e = p_judge_pos * p_human_pos + p_judge_neg * p_human_neg
    if p_e >= 1.0 or abs(1.0 - p_e) < 1e-12:
        raise ValueError("Cohen's kappa is undefined when p_e == 1")
    return (p_o - p_e) / (1.0 - p_e)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denom = sensitivity + specificity - 1.0
    if abs(denom) < 1e-12:
        val = 0.0
    else:
        val = (observed_rate + specificity - 1.0) / denom
    return max(0.0, min(1.0, val))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy import stats as sp_stats

    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)

    if len(a_arr) == 0 or np.array_equal(a_arr, b_arr):
        return (0.0, 0.0, 0.0)

    def diff_mean(x, y, axis=-1):
        return np.mean(x, axis=axis) - np.mean(y, axis=axis)

    random_state = np.random.default_rng(rng)
    res = sp_stats.bootstrap(
        (a_arr, b_arr),
        diff_mean,
        paired=True,
        method="percentile",
        n_resamples=n_resamples,
        random_state=random_state,
        confidence_level=confidence,
    )
    d = float(np.mean(a_arr) - np.mean(b_arr))
    lo = float(res.confidence_interval.low)
    hi = float(res.confidence_interval.high)
    return (d, lo, hi)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
