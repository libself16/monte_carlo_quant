from datetime import datetime
from pathlib import Path
import shutil

import config
from core.io import load_trade_data
from core.metrics import summarize_equity_paths
from core.monte_carlo import build_sample_indices, run_simulation_set
from core.report import save_excel_summary, save_equity_distribution_charts, save_text_report


def main():
    output_folder = Path(config.OUTPUT_FOLDER)
    output_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_output = output_folder / timestamp
    session_output.mkdir(parents=True, exist_ok=True)

    trades = load_trade_data(config)
    print(f"Loaded {len(trades)} trades from {config.INPUT_FOLDER}")

    if config.INPUT_FILE:
        source_file = Path(config.INPUT_FOLDER) / config.INPUT_FILE
        if source_file.exists():
            copied_input = session_output / source_file.name
            shutil.copy2(source_file, copied_input)
            print(f"Copied input file to: {copied_input}")

    r_values = trades["R"].to_numpy(dtype=float)
    sample_indices = build_sample_indices(len(r_values), config.SIMULATION_RUNS, config.RANDOM_SEED)
    results = run_simulation_set(
        r_values,
        config.RISK_RATIOS,
        sample_indices,
        config.COMPARE_FIXED_AND_COMPOUND,
        start_equity=config.INITIAL_CAPITAL,
    )

    summary_records = []
    for mode_name, mode_results in results.items():
        if mode_name == "risk_ratios":
            continue
        for ratio, equity_matrix in mode_results.items():
            record = summarize_equity_paths(
                equity_matrix,
                r_values,
                ratio,
                mode_name,
                initial_capital=config.INITIAL_CAPITAL,
                ruin_threshold=config.RUIN_THRESHOLD,
                display_range=config.DISPLAY_RANGE,
            )
            summary_records.append(record)

    if config.USE_EXCEL_OUTPUT:
        excel_path = save_excel_summary(summary_records, session_output)
        print(f"Excel summary written to: {excel_path}")

    if config.USE_PNG_OUTPUT:
        chart_paths = save_equity_distribution_charts(results, session_output, config)
        print(f"Distribution charts written to: {len(chart_paths)} files")

    if config.USE_TXT_REPORT:
        txt_path = save_text_report(summary_records, config, session_output)
        print(f"Text report written to: {txt_path}")

    print("Monte Carlo simulation complete.")


if __name__ == "__main__":
    main()
