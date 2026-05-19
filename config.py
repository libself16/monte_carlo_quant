from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FOLDER = BASE_DIR / "input"
INPUT_FILE = "data.csv"
OUTPUT_FOLDER = BASE_DIR / "output"

SIMULATION_RUNS = 10000
RISK_RATIOS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]
SYMBOL_FILTER = None

COMPARE_FIXED_AND_COMPOUND = True
RANDOM_SEED = 42
USE_EXCEL_OUTPUT = True
USE_PNG_OUTPUT = True
USE_TXT_REPORT = True
CSV_COLUMNS = {"symbol": "S", "return": "R"}

# 初始資金
INITIAL_CAPITAL = 40000
# 破產線
RUIN_THRESHOLD = 10000
# 顯示範圍（去頭去尾）
DISPLAY_RANGE = 1.0