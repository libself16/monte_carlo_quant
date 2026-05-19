import numpy as np


def compute_max_drawdown(equity):
    peak = np.maximum.accumulate(equity)
    drawdowns = (equity - peak) / peak
    return float(-np.min(drawdowns))


def compute_loss_streaks(equity):
    changes = np.diff(equity)
    losing = changes < 0
    if losing.size == 0:
        return 0
    max_streak = 0
    current = 0
    for step in losing:
        if step:
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0
    return max_streak


def compute_risk_of_ruin(final_equity, threshold=0.0):
    return float(np.mean(final_equity <= threshold))


def compute_probability_of_profit(final_equity, initial_capital):
    return float(np.mean(final_equity > initial_capital))


def compute_return_statistics(r_values, risk_ratio):
    r_values = np.asarray(r_values, dtype=float)
    bet = risk_ratio / 100.0
    returns = r_values * bet
    wins = returns[returns > 0.0]
    losses = returns[returns < 0.0]
    win_rate = float(np.mean(returns > 0.0))
    loss_rate = 1.0 - win_rate
    avg_win = float(np.mean(wins)) if wins.size else 0.0
    avg_loss = float(np.mean(losses)) if losses.size else 0.0
    expectancy = win_rate * avg_win + loss_rate * avg_loss
    profit_factor = float(np.sum(wins) / abs(np.sum(losses))) if losses.size else float("inf")
    return {
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "expectancy": expectancy,
        "profit_factor": profit_factor,
    }


def summarize_equity_paths(equity_matrix, r_values, risk_ratio, mode_name="fixed", initial_capital=100.0, ruin_threshold=0.0, display_range=0.8):
    final_values = equity_matrix[:, -1]
    max_dd = np.array([compute_max_drawdown(row) for row in equity_matrix], dtype=float)
    ruin_rate = compute_risk_of_ruin(final_values, ruin_threshold)
    profit_prob = compute_probability_of_profit(final_values, initial_capital)
    stats = compute_return_statistics(r_values, risk_ratio)
    sorted_values = np.sort(final_values)
    low_idx = int(np.floor((1.0 - display_range) / 2.0 * len(sorted_values)))
    high_idx = int(np.ceil((1.0 + display_range) / 2.0 * len(sorted_values))) - 1
    low_idx = max(0, low_idx)
    high_idx = min(len(sorted_values) - 1, high_idx)
    return {
        "mode": mode_name,
        "risk_ratio": risk_ratio,
        "initial_capital": initial_capital,
        "display_range": display_range,
        "ruin_threshold": ruin_threshold,
        "average_final_equity": float(np.mean(final_values)),
        "average_final_equity_pct": float((np.mean(final_values) - initial_capital) / initial_capital),
        "median_final_equity": float(np.median(final_values)),
        "median_final_equity_pct": float((np.median(final_values) - initial_capital) / initial_capital),
        "best_final_equity": float(np.max(final_values)),
        "best_final_equity_pct": float((np.max(final_values) - initial_capital) / initial_capital),
        "worst_final_equity": float(np.min(final_values)),
        "worst_final_equity_pct": float((np.min(final_values) - initial_capital) / initial_capital),
        "probability_of_profit": profit_prob,
        "risk_of_ruin": ruin_rate,
        "avg_max_drawdown": float(np.mean(max_dd)),
        "worst_max_drawdown": float(np.max(max_dd)),
        "best_max_drawdown": float(np.min(max_dd)),
        "avg_losing_streak": float(np.mean([compute_loss_streaks(row) for row in equity_matrix])),
        "worst_losing_streak": int(np.max([compute_loss_streaks(row) for row in equity_matrix])),
        "best_losing_streak": int(np.min([compute_loss_streaks(row) for row in equity_matrix])),
        **stats,
    }
