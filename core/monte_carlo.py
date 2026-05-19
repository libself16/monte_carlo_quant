import numpy as np


def build_sample_indices(n_trades, n_runs, random_seed=None):
    rng = np.random.default_rng(random_seed)
    return rng.integers(0, n_trades, size=(n_runs, n_trades), dtype=np.int64)


def simulate_equity_paths(r_values, risk_ratio, sample_indices, start_equity=100.0, compound=False):
    r_values = np.asarray(r_values, dtype=float)
    draws = r_values[sample_indices]
    bet = risk_ratio / 100.0

    if compound:
        equity = start_equity * np.cumprod(1.0 + draws * bet, axis=1)
    else:
        profit = np.cumsum(draws * bet, axis=1) * start_equity
        equity = start_equity + profit

    return equity


def run_simulation_set(r_values, risk_ratios, sample_indices, compare_compound=True, start_equity=100.0):
    results = {
        "fixed": {},
        "compound": {},
        "risk_ratios": list(risk_ratios),
    }
    for ratio in risk_ratios:
        results["fixed"][ratio] = simulate_equity_paths(r_values, ratio, sample_indices, start_equity=start_equity, compound=False)
        if compare_compound:
            results["compound"][ratio] = simulate_equity_paths(r_values, ratio, sample_indices, start_equity=start_equity, compound=True)
    return results
