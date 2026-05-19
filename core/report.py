from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl.styles import Alignment


def ensure_output_folder(path):
    output_path = Path(path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def save_excel_summary(summary_records, output_folder):
    output_path = ensure_output_folder(output_folder) / "monte_carlo_summary.xlsx"
    df = pd.DataFrame(summary_records)

    df["Average Final Equity (平均權益)"] = (
        df["average_final_equity"].map("{:.2f}".format)
        + " ("
        + df["average_final_equity_pct"].map("{:.2%}".format)
        + ")"
    )
    df["Median Final Equity (中位數權益)"] = (
        df["median_final_equity"].map("{:.2f}".format)
        + " ("
        + df["median_final_equity_pct"].map("{:.2%}".format)
        + ")"
    )
    df["Best Case / High Bound (最佳 / 上限)"] = (
        df["best_final_equity"].map("{:.2f}".format)
        + " ("
        + df["best_final_equity_pct"].map("{:.2%}".format)
        + ")"
    )
    df["Worst Case / Low Bound (最差 / 低限)"] = (
        df["worst_final_equity"].map("{:.2f}".format)
        + " ("
        + df["worst_final_equity_pct"].map("{:.2%}".format)
        + ")"
    )
    df["Avg Max Drawdown (平均最大回撤)"] = (
        (-df["avg_max_drawdown"] * df["initial_capital"]).map("{:.2f}".format)
        + " ("
        + (-df["avg_max_drawdown"]).map("{:.2%}".format)
        + ")"
    )
    df["Worst Max Drawdown (最差最大回撤)"] = (
        (-df["worst_max_drawdown"] * df["initial_capital"]).map("{:.2f}".format)
        + " ("
        + (-df["worst_max_drawdown"]).map("{:.2%}".format)
        + ")"
    )
    df["Best Max Drawdown (最小最大回撤)"] = (
        (-df["best_max_drawdown"] * df["initial_capital"]).map("{:.2f}".format)
        + " ("
        + (-df["best_max_drawdown"]).map("{:.2%}".format)
        + ")"
    )
    df["Probability of Profit (區間內勝率)"] = df["probability_of_profit"].map("{:.2%}".format)
    df["Avg Losing Streak (平均連敗次數)"] = df["avg_losing_streak"].map("{:.2f}".format)

    df = df[
        [
            "mode",
            "risk_ratio",
            "initial_capital",
            "display_range",
            "ruin_threshold",
            "Average Final Equity (平均權益)",
            "Median Final Equity (中位數權益)",
            "Best Case / High Bound (最佳 / 上限)",
            "Worst Case / Low Bound (最差 / 低限)",
            "Probability of Profit (區間內勝率)",
            "risk_of_ruin",
            "Avg Max Drawdown (平均最大回撤)",
            "Worst Max Drawdown (最差最大回撤)",
            "Best Max Drawdown (最小最大回撤)",
            "Avg Losing Streak (平均連敗次數)",
            "worst_losing_streak",
            "best_losing_streak",
        ]
    ]
    df.columns = [
        "模式",
        "風險比例 (%)",
        "Initial Capital (初始資金)",
        "Display Range (顯示範圍)",
        "Ruin Threshold (破產線)",
        "Average Final Equity (平均權益)",
        "Median Final Equity (中位數權益)",
        "Best Case / High Bound (最佳 / 上限)",
        "Worst Case / Low Bound (最差 / 低限)",
        "Probability of Profit (區間內勝率)",
        "Risk of Ruin (全樣本破產率)",
        "Avg Max Drawdown (平均最大回撤)",
        "Worst Max Drawdown (最差最大回撤)",
        "Best Max Drawdown (最小最大回撤)",
        "Avg Losing Streak (平均連敗次數)",
        "Worst Losing Streak (最大連敗次數)",
        "Best Losing Streak (最小連敗次數)",
    ]

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Summary")
        worksheet = writer.sheets["Summary"]
        center_align = Alignment(horizontal="center", vertical="center")
        for column_cells in worksheet.columns:
            column_letter = column_cells[0].column_letter
            max_length = max(
                len(str(cell.value)) if cell.value is not None else 0
                for cell in column_cells
            )
            worksheet.column_dimensions[column_letter].width = max_length + 2
            for cell in column_cells:
                cell.alignment = center_align
    return output_path


def save_text_report(summary_records, config, output_folder):
    output_path = ensure_output_folder(output_folder) / "monte_carlo_report.txt"
    lines = [
        "Monte Carlo Quant 報告",
        "========================",
        f"Input folder: {config.INPUT_FOLDER}",
        f"Input file: {config.INPUT_FILE}",
        f"Simulation runs: {config.SIMULATION_RUNS}",
        f"Risk ratios: {config.RISK_RATIOS}",
        f"Initial Capital (初始資金): {config.INITIAL_CAPITAL}",
        f"Ruin Threshold (破產線): {config.RUIN_THRESHOLD}",
        f"Display Range (顯示範圍): {config.DISPLAY_RANGE}",
        "",
        "Summary by mode and risk ratio:",
    ]
    for rec in summary_records:
        lines.append(f"- 模式: {rec['mode']} | 風險比例: {rec['risk_ratio']}%")
        lines.append(f"  Initial Capital (初始資金): {rec['initial_capital']:.2f}")
        lines.append(f"  Display Range (顯示範圍): {rec['display_range']:.2f}")
        lines.append(f"  Ruin Threshold (破產線): {rec['ruin_threshold']:.2f}")
        lines.append(f"  Average Final Equity (平均權益): {rec['average_final_equity']:.2f} ({rec['average_final_equity_pct']:+.2%})")
        lines.append(f"  Median Final Equity (中位數權益): {rec['median_final_equity']:.2f} ({rec['median_final_equity_pct']:+.2%})")
        lines.append(f"  Best Case / High Bound (最佳 / 上限): {rec['best_final_equity']:.2f} ({rec['best_final_equity_pct']:+.2%})")
        lines.append(f"  Worst Case / Low Bound (最差 / 下限): {rec['worst_final_equity']:.2f} ({rec['worst_final_equity_pct']:+.2%})")
        lines.append(f"  Probability of Profit (區間內勝率): {rec['probability_of_profit']:.2%}")
        lines.append(f"  Risk of Ruin (全樣本破產率): {rec['risk_of_ruin']:.2%}")
        lines.append(
            f"  Avg Max Drawdown (平均最大回撤): {-rec['avg_max_drawdown']*rec['initial_capital']:.2f} ({-rec['avg_max_drawdown']:.2%})"
        )
        lines.append(
            f"  Worst Max Drawdown (最差最大回撤): {-rec['worst_max_drawdown']*rec['initial_capital']:.2f} ({-rec['worst_max_drawdown']:.2%})"
        )
        lines.append(
            f"  Best Max Drawdown (最小最大回撤): {-rec['best_max_drawdown']*rec['initial_capital']:.2f} ({-rec['best_max_drawdown']:.2%})"
        )
        lines.append(f"  Avg Losing Streak (平均連敗次數): {rec['avg_losing_streak']:.2f}")
        lines.append(f"  Worst Losing Streak (最大連敗次數): {rec['worst_losing_streak']}")
        lines.append(f"  Best Losing Streak (最小連敗次數): {rec['best_losing_streak']}")
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def save_equity_distribution_charts(equity_results, output_folder, config):
    output_folder = ensure_output_folder(output_folder) / "plots"
    output_folder.mkdir(parents=True, exist_ok=True)
    saved_paths = []
    for mode_name, mode_results in equity_results.items():
        if mode_name == "risk_ratios":
            continue
        for ratio, equity_matrix in mode_results.items():
            final_values = equity_matrix[:, -1]
            best_idx = int(np.argmax(final_values))
            worst_idx = int(np.argmin(final_values))
            trade_count = equity_matrix.shape[1]
            x = range(trade_count)

            plt.figure(figsize=(14, 8))
            plt.plot(
                x,
                equity_matrix.T,
                color="tab:blue",
                linewidth=0.25,
                alpha=0.03,
                label="Monte Carlo paths",
            )
            plt.plot(
                x,
                equity_matrix[best_idx],
                color="green",
                linewidth=2.5,
                label="Best Case",
            )
            plt.plot(
                x,
                equity_matrix[worst_idx],
                color="red",
                linewidth=2.5,
                label="Worst Case",
            )
            plt.title(f"{mode_name.capitalize()} {ratio:.2f}% - Equity Paths")
            plt.xlabel("Trade Number")
            plt.ylabel("Account Equity")
            plt.grid(True, linestyle="--", alpha=0.4)
            plt.legend(loc="upper left")
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            chart_path = output_folder / f"monte_carlo_{mode_name}_{ratio:.2f}.png"
            plt.savefig(chart_path)
            plt.close()
            saved_paths.append(chart_path)
    return saved_paths
